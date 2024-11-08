from netbox.plugins import PluginMenuItem
from netbox.plugins import PluginMenuButton, PluginMenuItem

risk_buttons = [
    PluginMenuButton(
        link='plugins:risks:risk_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]
risk_rel_buttons = [
    PluginMenuButton(
        link='plugins:risks:riskrelation_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:risks:risk_list',
        link_text='Risks',
        buttons=risk_buttons
    ),
    PluginMenuItem(
        link='plugins:risks:riskrelation_list',
        link_text='Risk Relations',
        buttons=risk_rel_buttons
    ),
)
