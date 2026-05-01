import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable

from .models import AVPortAssignment, AVPortProfile


class AVPortProfileTable(NetBoxTable):
    name = tables.Column(linkify=True)
    signal = ChoiceFieldColumn()
    rate = ChoiceFieldColumn()
    connector = ChoiceFieldColumn()
    direction = ChoiceFieldColumn()
    gender = ChoiceFieldColumn()
    assignment_count = tables.Column(verbose_name="Assignments")

    class Meta(NetBoxTable.Meta):
        model = AVPortProfile
        fields = (
            "pk",
            "id",
            "name",
            "signal",
            "rate",
            "connector",
            "direction",
            "gender",
            "channel_count",
            "assignment_count",
            "description",
            "comments",
            "tags",
            "actions",
        )
        default_columns = (
            "name",
            "signal",
            "rate",
            "connector",
            "direction",
            "assignment_count",
            "actions",
        )


class AVPortAssignmentTable(NetBoxTable):
    profile = tables.Column(linkify=True)
    endpoint = tables.Column(empty_values=(), linkify=True)
    endpoint_type = tables.Column(empty_values=())
    device = tables.Column(empty_values=(), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = AVPortAssignment
        fields = (
            "pk",
            "id",
            "profile",
            "endpoint",
            "endpoint_type",
            "device",
            "interface",
            "front_port",
            "rear_port",
            "comments",
            "tags",
            "actions",
        )
        default_columns = (
            "profile",
            "endpoint",
            "endpoint_type",
            "device",
            "actions",
        )

    def render_endpoint(self, record):
        return record.endpoint

    def render_endpoint_type(self, record):
        return record.endpoint_type

    def render_device(self, record):
        return record.device
