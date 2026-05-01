from netbox.api.serializers import NetBoxModelSerializer
from rest_framework import serializers

from ..models import AVPortAssignment, AVPortProfile


class AVPortProfileSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_av_plugin-api:avportprofile-detail",
    )
    assignment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = AVPortProfile
        fields = (
            "id",
            "url",
            "display",
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
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "name")


class AVPortAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_av_plugin-api:avportassignment-detail",
    )
    endpoint = serializers.SerializerMethodField(read_only=True)
    endpoint_type = serializers.CharField(read_only=True)
    device = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AVPortAssignment
        fields = (
            "id",
            "url",
            "display",
            "profile",
            "endpoint",
            "endpoint_type",
            "device",
            "interface",
            "front_port",
            "rear_port",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "url", "display", "profile")

    def get_endpoint(self, obj):
        endpoint = obj.endpoint
        if endpoint is None:
            return None
        return str(endpoint)
