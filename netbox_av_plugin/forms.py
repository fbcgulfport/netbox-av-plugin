from django import forms
from dcim.models import FrontPort, Interface, RearPort
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet

from .choices import AVConnectorChoices, AVDirectionChoices, AVGenderChoices, AVRateChoices, AVSignalChoices
from .models import AVPortAssignment, AVPortProfile


class AVPortProfileForm(NetBoxModelForm):
    comments = CommentField()

    class Meta:
        model = AVPortProfile
        fields = (
            "name",
            "signal",
            "rate",
            "connector",
            "direction",
            "gender",
            "channel_count",
            "description",
            "comments",
            "tags",
        )


class AVPortAssignmentForm(NetBoxModelForm):
    profile = DynamicModelChoiceField(
        queryset=AVPortProfile.objects.all(),
    )
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
    )
    front_port = DynamicModelChoiceField(
        queryset=FrontPort.objects.all(),
        required=False,
    )
    rear_port = DynamicModelChoiceField(
        queryset=RearPort.objects.all(),
        required=False,
    )
    comments = CommentField()

    class Meta:
        model = AVPortAssignment
        fields = (
            "profile",
            "interface",
            "front_port",
            "rear_port",
            "comments",
            "tags",
        )


class AVPortProfileFilterForm(NetBoxModelFilterSetForm):
    model = AVPortProfile
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("signal", "rate", "connector", "direction", "gender", name="AV"),
    )

    signal = forms.MultipleChoiceField(
        choices=AVSignalChoices,
        required=False,
    )
    rate = forms.MultipleChoiceField(
        choices=AVRateChoices,
        required=False,
    )
    connector = forms.MultipleChoiceField(
        choices=AVConnectorChoices,
        required=False,
    )
    direction = forms.MultipleChoiceField(
        choices=AVDirectionChoices,
        required=False,
    )
    gender = forms.MultipleChoiceField(
        choices=AVGenderChoices,
        required=False,
    )
    tag = TagFilterField(model)


class AVPortAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = AVPortAssignment
    fieldsets = (
        FieldSet("q", "filter_id", "tag"),
        FieldSet("profile", "interface_id", "front_port_id", "rear_port_id", name="Assignment"),
    )

    profile = forms.ModelMultipleChoiceField(
        queryset=AVPortProfile.objects.all(),
        required=False,
    )
    interface_id = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="Interface",
    )
    front_port_id = DynamicModelMultipleChoiceField(
        queryset=FrontPort.objects.all(),
        required=False,
        label="Front Port",
    )
    rear_port_id = DynamicModelMultipleChoiceField(
        queryset=RearPort.objects.all(),
        required=False,
        label="Rear Port",
    )
    tag = TagFilterField(model)
