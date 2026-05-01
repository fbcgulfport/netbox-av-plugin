from netbox.search import SearchIndex, register_search

from .models import AVPortAssignment, AVPortProfile


@register_search
class AVPortProfileIndex(SearchIndex):
    model = AVPortProfile
    fields = (
        ("name", 100),
        ("description", 500),
        ("comments", 5000),
    )
    display_attrs = ("name", "signal", "rate", "connector", "direction")


@register_search
class AVPortAssignmentIndex(SearchIndex):
    model = AVPortAssignment
    fields = (("comments", 5000),)
    display_attrs = ("profile", "endpoint_type", "device")
