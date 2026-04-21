GPU_PROFILES = {
    "Gaming": {
        "prefixes": ["GeForce RTX", "GeForce GTX", "Radeon RX", "Arc A", "Arc B"],
        "prioritize_vram": False,
    },
    "Machine Learning": {
        "prefixes": [
            "GeForce RTX 20", "GeForce RTX 30", "GeForce RTX 40", "GeForce RTX 50",
            "Quadro RTX", "RTX A", "RTX 2000 Ada", "RTX 2000E Ada", "RTX 4000 Ada",
            "RTX 4000 SFF Ada", "RTX 4500 Ada", "RTX 5000 Ada", "RTX 6000 Ada", "TITAN RTX",
        ],
        "prioritize_vram": True,
    },
    "Video Editing": {
        "prefixes": [
            "GeForce RTX", "GeForce GTX 16", "GeForce GTX 10", "Quadro RTX", "RTX A",
            "RTX 2000", "RTX 4000", "RTX 4500", "RTX 5000", "RTX 6000",
            "Radeon RX 7", "Radeon RX 6", "Radeon RX 5",
        ],
        "prioritize_vram": False,
    },
}


BUDGET_WEIGHTS = {
    "Gaming": {"GPU": 0.45, "CPU": 0.25, "RAM": 0.08, "Motherboard": 0.10, "Storage": 0.07, "PSU": 0.05},
    "Video Editing": {"GPU": 0.32, "CPU": 0.27, "RAM": 0.14, "Motherboard": 0.08, "Storage": 0.12, "PSU": 0.06},
    "Machine Learning": {"GPU": 0.52, "CPU": 0.16, "RAM": 0.11, "Motherboard": 0.07, "Storage": 0.07, "PSU": 0.07},
}


SOCKET_DDR_MAP = {
    "AM4":    ["DDR4"],
    "AM5":    ["DDR5"],
    "sTR4":   ["DDR4"],
    "sTRX4":  ["DDR4"],
    "sWRX8":  ["DDR4"],
    "LGA1155": ["DDR3"],
    "LGA1150": ["DDR3"],
    "LGA1151": ["DDR4"],
    "LGA1200": ["DDR4"],
    "LGA1700": ["DDR4", "DDR5"],
    "LGA1851": ["DDR5"],
}


GPU_BRAND_PREFIXES = {
    "NVIDIA": ["GeForce RTX", "GeForce GTX"],
    "AMD": ["Radeon RX"],
    "INTEL": ["Arc A", "Arc B"],
}
CPU_BRANDS = ["AMD", "INTEL"]
ACCEPTABLE_PSU_TIERS = ["A", "B", "C"]
ALTERNATIVE_PSU_TIERS = ["A", "B"]
COMPONENT_PRICE_RANGE = (0.85, 1.15)
STORAGE_PRICE_RANGE = (0.70, 1.30)
OTHER_COMPONENT_WATTAGE = 100
PSU_POWER_MULTIPLIER = 1.5
STORAGE_INTERFACE_RANKS = (
    ('PCIe 5.0', 5), ('PCIe 4.0', 4), ('PCIe 3.0', 3), ('PCIe', 2), ('SATA', 1),
)
