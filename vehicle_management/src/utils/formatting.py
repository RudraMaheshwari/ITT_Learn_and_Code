from ..config.constants import ENERGY_LEVEL_NOTICE_TEMPLATE

def energy_level_notice_line(
    past_action: str, quantity_label: str, level_percent: float
) -> str:
    return ENERGY_LEVEL_NOTICE_TEMPLATE.format(
        past_action=past_action,
        quantity_label=quantity_label,
        level_percent=level_percent,
    )
