import json
import os
from typing import List

from openai import OpenAI

from app.dto.build import ComponentSummary


DEFAULT_GAMES = (
    "Minecraft (Java Edition)",
    "Fortnite (DirectX 12)",
    "Cyberpunk 2077 (Ray Tracing OFF)",
)
DISCLAIMER = (
    "Disclaimer: The FPS estimates shown are based on AI-generated estimations "
    "and may not match actual in-game performance."
)
PROMPT_TEMPLATE = """Estimate FPS for exactly {game_count} at 1080p, 1440p, and 4K (2160p) resolutions across Low, Medium, High, and Ultra quality settings.

    The PC has these components:
    {parts_description}

    {games_description}

    RULES:
    - Use the exact GPU and CPU listed. Base FPS on real-world benchmarks.
    {extra_rules}- Keep FPS ranges tight (max 15-30 FPS spread).

    Respond ONLY with valid JSON, no markdown:
    {{
      "estimates": [
        {{
          "game": {example_game},
          "resolutions": [
            {{
              "resolution": "1080p",
              "low": {{"min": 200, "max": 230}},
              "medium": {{"min": 160, "max": 190}},
              "high": {{"min": 120, "max": 150}},
              "ultra": {{"min": 90, "max": 110}}
            }},
            {{
              "resolution": "1440p",
              "low": {{"min": 150, "max": 180}},
              "medium": {{"min": 120, "max": 150}},
              "high": {{"min": 90, "max": 110}},
              "ultra": {{"min": 60, "max": 80}}
            }},
            {{
              "resolution": "4K",
              "low": {{"min": 100, "max": 130}},
              "medium": {{"min": 80, "max": 100}},
              "high": {{"min": 55, "max": 70}},
              "ultra": {{"min": 35, "max": 50}}
            }}
          ]
        }}
      ]
    }}

    The numbers above are EXAMPLES ONLY. Replace with accurate estimates for the EXACT hardware listed."""


def request_estimates(api_key: str, prompt: str) -> dict:
    """Call the FPS provider and decode its JSON response."""
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a PC hardware performance analyst that estimates FPS for games. Respond only with valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=2000,
    )
    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(content)


def estimate_fps(components: List[ComponentSummary]) -> dict:
    parts_description = "\n".join(
        f"- {part.type.upper()}: {part.name} - {part.specs.model_dump_json(exclude_none=True)}"
        for part in components if part.type.upper() in {"GPU", "CPU", "RAM"}
    )
    return request_fps(parts_description, DEFAULT_GAMES)


def estimate_fps_standalone(cpu_name: str, gpu_name: str, game: str) -> dict:
    parts_description = f"- CPU: {cpu_name}\n    - GPU: {gpu_name}"
    return request_fps(parts_description, (game,))


def request_fps(parts_description: str, games: tuple[str, ...]) -> dict:
    standalone = len(games) == 1
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or (standalone and api_key == "your-openai-api-key-here"):
        message = "OpenAI API key not configured"
        if standalone:
            message += ". Please add your key to the .env file."
        return {"estimates": [], "disclaimer": message}

    games_description = (
        f"Game: {games[0]}" if standalone else "Games:\n    " + "\n    ".join(
            f"{index}. {game}" for index, game in enumerate(games, start=1)
        )
    )
    extra_rules = "" if standalone else (
        "- Cyberpunk 2077: scale FPS based on the GPU "
        "(e.g., RTX 5070 Ti ~130-160 FPS at 1080p Ultra, RT off).\n    "
    )
    prompt = PROMPT_TEMPLATE.format(
        game_count="this 1 game" if standalone else f"these {len(games)} games",
        parts_description=parts_description,
        games_description=games_description,
        extra_rules=extra_rules,
        example_game=json.dumps(games[0] if standalone else "Game Name"),
    )

    try:
        result = request_estimates(api_key, prompt)
        result["disclaimer"] = DISCLAIMER
        return result
    except Exception as error:
        return {"estimates": [], "disclaimer": f"Failed to generate FPS estimates: {error}"}
