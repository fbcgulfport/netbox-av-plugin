import django.db.models.deletion
import netbox.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models
from django.db.models import Q


DEFAULT_PROFILES = (
    ("SD-SDI Input over BNC", "sdi", "sd-sdi", "bnc", "input"),
    ("SD-SDI Output over BNC", "sdi", "sd-sdi", "bnc", "output"),
    ("HD-SDI Input over BNC", "sdi", "hd-sdi", "bnc", "input"),
    ("HD-SDI Output over BNC", "sdi", "hd-sdi", "bnc", "output"),
    ("3G-SDI Input over BNC", "sdi", "3g-sdi", "bnc", "input"),
    ("3G-SDI Output over BNC", "sdi", "3g-sdi", "bnc", "output"),
    ("6G-SDI Input over BNC", "sdi", "6g-sdi", "bnc", "input"),
    ("6G-SDI Output over BNC", "sdi", "6g-sdi", "bnc", "output"),
    ("XLR Input", "analog-audio", "", "xlr", "input"),
    ("XLR Output", "analog-audio", "", "xlr", "output"),
    ("DMX 3-pin Input", "dmx", "", "dmx-3-pin", "input"),
    ("DMX 3-pin Output", "dmx", "", "dmx-3-pin", "output"),
    ("DMX 3-pin Thru", "dmx", "", "dmx-3-pin", "thru"),
    ("DMX 5-pin Input", "dmx", "", "dmx-5-pin", "input"),
    ("DMX 5-pin Output", "dmx", "", "dmx-5-pin", "output"),
    ("DMX 5-pin Thru", "dmx", "", "dmx-5-pin", "thru"),
    ("HDMI Input", "hdmi", "", "hdmi", "input"),
    ("HDMI Output", "hdmi", "", "hdmi", "output"),
    ('1/4" Headphone Output', "analog-audio", "", "trs-1-4", "output"),
    ("3.5mm Headphone Output", "analog-audio", "", "trs-3-5", "output"),
    ("Speakon Output", "speaker", "", "speakon", "output"),
    ("Timecode Input over BNC", "timecode", "", "bnc", "input"),
    ("Timecode Output over BNC", "timecode", "", "bnc", "output"),
    ("Genlock Input over BNC", "genlock", "", "bnc", "input"),
    ("Genlock Output over BNC", "genlock", "", "bnc", "output"),
    ("RS-422 Input over DE-9", "rs-422", "", "de-9", "input"),
    ("RS-422 Output over DE-9", "rs-422", "", "de-9", "output"),
    ("RS-422 Bidirectional over DE-9", "rs-422", "", "de-9", "bidirectional"),
)


def create_default_profiles(apps, schema_editor):
    profile_model = apps.get_model("netbox_av_plugin", "AVPortProfile")
    for name, signal, rate, connector, direction in DEFAULT_PROFILES:
        profile_model.objects.get_or_create(
            name=name,
            defaults={
                "signal": signal,
                "rate": rate,
                "connector": connector,
                "direction": direction,
                "gender": "unknown",
            },
        )


def remove_default_profiles(apps, schema_editor):
    profile_model = apps.get_model("netbox_av_plugin", "AVPortProfile")
    profile_model.objects.filter(name__in=[profile[0] for profile in DEFAULT_PROFILES]).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("dcim", "0215_rackreservation_status"),
        ("extras", "0132_configcontextprofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="AVPortProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("signal", models.CharField(max_length=50)),
                (
                    "rate",
                    models.CharField(
                        blank=True,
                        help_text="Optional signal rate; leave blank for generic compatibility.",
                        max_length=50,
                    ),
                ),
                ("connector", models.CharField(max_length=50)),
                ("direction", models.CharField(max_length=50)),
                ("gender", models.CharField(default="unknown", max_length=50)),
                ("channel_count", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("comments", models.TextField(blank=True)),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={
                "verbose_name": "AV Port Profile",
                "verbose_name_plural": "AV Port Profiles",
                "ordering": ("signal", "connector", "direction", "name"),
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AVPortAssignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ("comments", models.TextField(blank=True)),
                (
                    "front_port",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="av_assignments",
                        to="dcim.frontport",
                    ),
                ),
                (
                    "interface",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="av_assignments",
                        to="dcim.interface",
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="assignments",
                        to="netbox_av_plugin.avportprofile",
                    ),
                ),
                (
                    "rear_port",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="av_assignments",
                        to="dcim.rearport",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
            ],
            options={
                "verbose_name": "AV Port Assignment",
                "verbose_name_plural": "AV Port Assignments",
                "ordering": ("interface", "front_port", "rear_port", "profile"),
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name="avportassignment",
            constraint=models.CheckConstraint(
                name="netbox_av_plugin_avportassignment_one_endpoint",
                check=(
                    Q(interface__isnull=False, front_port__isnull=True, rear_port__isnull=True)
                    | Q(interface__isnull=True, front_port__isnull=False, rear_port__isnull=True)
                    | Q(interface__isnull=True, front_port__isnull=True, rear_port__isnull=False)
                ),
            ),
        ),
        migrations.AddConstraint(
            model_name="avportassignment",
            constraint=models.UniqueConstraint(
                fields=("interface",),
                condition=Q(interface__isnull=False),
                name="netbox_av_plugin_avportassignment_unique_interface",
            ),
        ),
        migrations.AddConstraint(
            model_name="avportassignment",
            constraint=models.UniqueConstraint(
                fields=("front_port",),
                condition=Q(front_port__isnull=False),
                name="netbox_av_plugin_avportassignment_unique_front_port",
            ),
        ),
        migrations.AddConstraint(
            model_name="avportassignment",
            constraint=models.UniqueConstraint(
                fields=("rear_port",),
                condition=Q(rear_port__isnull=False),
                name="netbox_av_plugin_avportassignment_unique_rear_port",
            ),
        ),
        migrations.RunPython(create_default_profiles, remove_default_profiles),
    ]
