__version__ = "0.1.0"

from netbox.plugins import PluginConfig


class NetBoxAVPluginConfig(PluginConfig):
    name = "netbox_av_plugin"
    verbose_name = "NetBox AV Plugin"
    description = "AV metadata and cable validation for NetBox endpoints"
    version = __version__
    base_url = "netbox-av-plugin"
    min_version = "4.4.0"


config = NetBoxAVPluginConfig
