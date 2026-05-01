from django.db.models import Q
import django_filters
from dcim.models import FrontPort, Interface, RearPort
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filtersets import register_filterset

from .models import AVPortAssignment, AVPortProfile


@register_filterset
class AVPortProfileFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = AVPortProfile
        fields = (
            "id",
            "name",
            "signal",
            "rate",
            "connector",
            "direction",
            "gender",
            "channel_count",
        )

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(comments__icontains=value)
        )


@register_filterset
class AVPortAssignmentFilterSet(NetBoxModelFilterSet):
    interface_id = django_filters.ModelMultipleChoiceFilter(
        field_name="interface",
        queryset=Interface.objects.all(),
        to_field_name="id",
        label="Interface ID",
    )
    front_port_id = django_filters.ModelMultipleChoiceFilter(
        field_name="front_port",
        queryset=FrontPort.objects.all(),
        to_field_name="id",
        label="Front Port ID",
    )
    rear_port_id = django_filters.ModelMultipleChoiceFilter(
        field_name="rear_port",
        queryset=RearPort.objects.all(),
        to_field_name="id",
        label="Rear Port ID",
    )

    class Meta:
        model = AVPortAssignment
        fields = ("id", "profile", "interface", "front_port", "rear_port")

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(profile__name__icontains=value)
            | Q(interface__name__icontains=value)
            | Q(front_port__name__icontains=value)
            | Q(rear_port__name__icontains=value)
            | Q(comments__icontains=value)
        )
