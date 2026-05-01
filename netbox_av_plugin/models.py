from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from netbox.models import NetBoxModel

from .choices import (
    AVConnectorChoices,
    AVDirectionChoices,
    AVGenderChoices,
    AVRateChoices,
    AVSignalChoices,
)


class AVPortProfile(NetBoxModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    signal = models.CharField(
        max_length=50,
        choices=AVSignalChoices,
    )
    rate = models.CharField(
        max_length=50,
        choices=AVRateChoices,
        blank=True,
        help_text="Optional signal rate; leave blank for generic compatibility.",
    )
    connector = models.CharField(
        max_length=50,
        choices=AVConnectorChoices,
    )
    direction = models.CharField(
        max_length=50,
        choices=AVDirectionChoices,
    )
    gender = models.CharField(
        max_length=50,
        choices=AVGenderChoices,
        default=AVGenderChoices.GENDER_UNKNOWN,
    )
    channel_count = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=200,
        blank=True,
    )
    comments = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ("signal", "connector", "direction", "name")
        verbose_name = "AV Port Profile"
        verbose_name_plural = "AV Port Profiles"

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.signal == AVSignalChoices.SIGNAL_SDI:
            if self.connector != AVConnectorChoices.CONNECTOR_BNC:
                raise ValidationError("SDI profiles must use BNC.")
            if not self.rate:
                raise ValidationError("SDI profiles must specify an SDI rate.")
        elif self.rate:
            raise ValidationError("Only SDI profiles may specify an SDI rate.")

        valid_connectors = {
            AVSignalChoices.SIGNAL_ANALOG_AUDIO: {
                AVConnectorChoices.CONNECTOR_XLR,
                AVConnectorChoices.CONNECTOR_TRS_1_4,
                AVConnectorChoices.CONNECTOR_TRS_3_5,
            },
            AVSignalChoices.SIGNAL_DMX: {
                AVConnectorChoices.CONNECTOR_DMX_3_PIN,
                AVConnectorChoices.CONNECTOR_DMX_5_PIN,
            },
            AVSignalChoices.SIGNAL_HDMI: {AVConnectorChoices.CONNECTOR_HDMI},
            AVSignalChoices.SIGNAL_SPEAKER: {AVConnectorChoices.CONNECTOR_SPEAKON},
            AVSignalChoices.SIGNAL_TIMECODE: {AVConnectorChoices.CONNECTOR_BNC},
            AVSignalChoices.SIGNAL_GENLOCK: {AVConnectorChoices.CONNECTOR_BNC},
            AVSignalChoices.SIGNAL_RS_422: {AVConnectorChoices.CONNECTOR_DE_9},
        }
        if self.signal in valid_connectors and self.connector not in valid_connectors[self.signal]:
            raise ValidationError("Connector does not match the selected AV signal.")

    def get_absolute_url(self):
        return reverse("plugins:netbox_av_plugin:avportprofile", args=[self.pk])

    def get_signal_color(self):
        return AVSignalChoices.colors.get(self.signal)

    def get_connector_color(self):
        return AVConnectorChoices.colors.get(self.connector)

    def get_direction_color(self):
        return AVDirectionChoices.colors.get(self.direction)


class AVPortAssignment(NetBoxModel):
    profile = models.ForeignKey(
        to="netbox_av_plugin.AVPortProfile",
        on_delete=models.PROTECT,
        related_name="assignments",
    )
    interface = models.ForeignKey(
        to="dcim.Interface",
        on_delete=models.CASCADE,
        related_name="av_assignments",
        blank=True,
        null=True,
    )
    front_port = models.ForeignKey(
        to="dcim.FrontPort",
        on_delete=models.CASCADE,
        related_name="av_assignments",
        blank=True,
        null=True,
    )
    rear_port = models.ForeignKey(
        to="dcim.RearPort",
        on_delete=models.CASCADE,
        related_name="av_assignments",
        blank=True,
        null=True,
    )
    comments = models.TextField(
        blank=True,
    )

    clone_fields = ("profile",)

    class Meta:
        ordering = ("interface", "front_port", "rear_port", "profile")
        verbose_name = "AV Port Assignment"
        verbose_name_plural = "AV Port Assignments"
        constraints = (
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_one_endpoint",
                check=(
                    Q(interface__isnull=False, front_port__isnull=True, rear_port__isnull=True)
                    | Q(interface__isnull=True, front_port__isnull=False, rear_port__isnull=True)
                    | Q(interface__isnull=True, front_port__isnull=True, rear_port__isnull=False)
                ),
            ),
            models.UniqueConstraint(
                fields=("interface",),
                condition=Q(interface__isnull=False),
                name="%(app_label)s_%(class)s_unique_interface",
            ),
            models.UniqueConstraint(
                fields=("front_port",),
                condition=Q(front_port__isnull=False),
                name="%(app_label)s_%(class)s_unique_front_port",
            ),
            models.UniqueConstraint(
                fields=("rear_port",),
                condition=Q(rear_port__isnull=False),
                name="%(app_label)s_%(class)s_unique_rear_port",
            ),
        )

    def __str__(self):
        return f"{self.endpoint} - {self.profile}"

    def clean(self):
        super().clean()
        endpoint_count = sum(
            value is not None
            for value in (self.interface_id, self.front_port_id, self.rear_port_id)
        )
        if endpoint_count != 1:
            raise ValidationError("Select exactly one endpoint: interface, front port, or rear port.")

    def get_absolute_url(self):
        return reverse("plugins:netbox_av_plugin:avportassignment", args=[self.pk])

    @property
    def endpoint(self):
        return self.interface or self.front_port or self.rear_port

    @property
    def endpoint_type(self):
        endpoint = self.endpoint
        if endpoint is None:
            return ""
        return endpoint._meta.verbose_name.title()

    @property
    def device(self):
        endpoint = self.endpoint
        if endpoint is None:
            return None
        return endpoint.device
