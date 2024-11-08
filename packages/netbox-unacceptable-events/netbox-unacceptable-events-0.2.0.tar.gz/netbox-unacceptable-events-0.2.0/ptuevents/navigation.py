from netbox.plugins import PluginMenuItem
from netbox.plugins import PluginMenuButton, PluginMenuItem


PTUEvent_buttons = [
    PluginMenuButton(
        link='plugins:ptuevents:ptuevent_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]
PTUEvent_rel_buttons = [
    PluginMenuButton(
        link='plugins:ptuevents:ptueventrelation_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

appsystem_buttons = [
    PluginMenuButton(
        link='plugins:ptuevents:ptappsystem_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

PTUsers_buttons = [
    PluginMenuButton(
        link='plugins:ptuevents:ptusers_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

PTWorkstations_buttons = [
    PluginMenuButton(
        link='plugins:ptuevents:ptworkstations_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:ptuevents:ptuevent_list',
        link_text='Events',
        buttons=PTUEvent_buttons
    ),
    PluginMenuItem(
        link='plugins:ptuevents:ptueventrelation_list',
        link_text='Event Relations',
        buttons=PTUEvent_rel_buttons
    ),
    PluginMenuItem(
        link='plugins:ptuevents:ptappsystem_list',
        link_text='App Systems',
        buttons=appsystem_buttons
    ),
    PluginMenuItem(
        link='plugins:ptuevents:ptusers_list',
        link_text='Users',
        buttons=PTUsers_buttons
    ),
    PluginMenuItem(
        link='plugins:ptuevents:ptworkstations_list',
        link_text='Workstations',
        buttons=PTWorkstations_buttons
    ),
)
