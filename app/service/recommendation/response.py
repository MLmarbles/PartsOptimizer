from app.database import Base
from app.dto.build import AlternativeSummary, BuildResponse, ComponentSpecs, ComponentSummary


SPEC_FIELDS = {
    "GPU": ("vram_gb", "benchmark_score"),
    "CPU": ("cores", "single_core_score", "multi_core_score"),
    "RAM": ("capacity_gb", "type", "speed_mhz"),
    "Motherboard": ("socket", "form_factor"),
    "Storage": ("capacity_gb", "type", "interface"),
    "PSU": ("wattage", "efficiency_rating"),
}


def component_specs(component_type: str, component: Base) -> ComponentSpecs:
    return ComponentSpecs(**{
        field: getattr(component, field) for field in SPEC_FIELDS[component_type]
    })


def build_response(
    selected: dict[str, Base | None],
    alternatives: dict[str, list[tuple[str, Base]]],
    budget: int,
    use_case: str,
) -> BuildResponse:
    components = []
    for component_type, component in selected.items():
        if component is None:
            continue
        alternative_summaries = [
            AlternativeSummary(
                brand=brand,
                name=alternative.name,
                price=alternative.price or 0,
                specs=component_specs(component_type, alternative),
            )
            for brand, alternative in alternatives.get(component_type, [])
        ]
        components.append(ComponentSummary(
            type=component_type,
            name=component.name,
            price=component.price or 0,
            specs=component_specs(component_type, component),
            tier=component.tier if component_type == "PSU" else None,
            alternatives=alternative_summaries or None,
        ))

    total_price = round(sum(component.price for component in components), 2)
    return BuildResponse(
        components=components,
        total_price=total_price,
        remaining_budget=round(budget - total_price, 2),
        use_case=use_case,
    )
