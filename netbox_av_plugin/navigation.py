from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

profile_buttons = [
    PluginMenuButton(
        link="plugins:netbox_av_plugin:avportprofile_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        permissions=["netbox_av_plugin.add_avportprofile"],
    )
]

assignment_buttons = [
    PluginMenuButton(
        link="plugins:netbox_av_plugin:avportassignment_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
        permissions=["netbox_av_plugin.add_avportassignment"],
    )
]

profile_item = PluginMenuItem(
    link="plugins:netbox_av_plugin:avportprofile_list",
    link_text="Port Profiles",
    permissions=["netbox_av_plugin.view_avportprofile"],
    buttons=profile_buttons,
)

assignment_item = PluginMenuItem(
    link="plugins:netbox_av_plugin:avportassignment_list",
    link_text="Port Assignments",
    permissions=["netbox_av_plugin.view_avportassignment"],
    buttons=assignment_buttons,
)

menu = PluginMenu(
    label="AV",
    groups=(("AV", (profile_item, assignment_item)),),
    icon_class="mdi mdi-video-input-component",
)
