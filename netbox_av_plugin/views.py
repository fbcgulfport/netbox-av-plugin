from django.db.models import Count, Q
from dcim.models import Device
from netbox.views import generic
from utilities.views import ViewTab, register_model_view

from . import filtersets, forms, models, tables


@register_model_view(models.AVPortProfile)
class AVPortProfileView(generic.ObjectView):
    queryset = models.AVPortProfile.objects.all()

    def get_extra_context(self, request, instance):
        assignments = instance.assignments.restrict(request.user, "view")
        assignments_table = tables.AVPortAssignmentTable(assignments)
        assignments_table.columns.hide("profile")
        assignments_table.configure(request)
        return {"assignments_table": assignments_table}


@register_model_view(models.AVPortProfile, name="list", path="", detail=False)
class AVPortProfileListView(generic.ObjectListView):
    queryset = models.AVPortProfile.objects.annotate(assignment_count=Count("assignments"))
    table = tables.AVPortProfileTable
    filterset = filtersets.AVPortProfileFilterSet
    filterset_form = forms.AVPortProfileFilterForm


@register_model_view(models.AVPortProfile, name="add", detail=False)
@register_model_view(models.AVPortProfile, name="edit")
class AVPortProfileEditView(generic.ObjectEditView):
    queryset = models.AVPortProfile.objects.all()
    form = forms.AVPortProfileForm


@register_model_view(models.AVPortProfile, name="delete")
class AVPortProfileDeleteView(generic.ObjectDeleteView):
    queryset = models.AVPortProfile.objects.all()


@register_model_view(models.AVPortAssignment)
class AVPortAssignmentView(generic.ObjectView):
    queryset = models.AVPortAssignment.objects.select_related(
        "profile",
        "interface__device",
        "front_port__device",
        "rear_port__device",
    )


@register_model_view(models.AVPortAssignment, name="list", path="", detail=False)
class AVPortAssignmentListView(generic.ObjectListView):
    queryset = models.AVPortAssignment.objects.select_related(
        "profile",
        "interface__device",
        "front_port__device",
        "rear_port__device",
    )
    table = tables.AVPortAssignmentTable
    filterset = filtersets.AVPortAssignmentFilterSet
    filterset_form = forms.AVPortAssignmentFilterForm


@register_model_view(models.AVPortAssignment, name="add", detail=False)
@register_model_view(models.AVPortAssignment, name="edit")
class AVPortAssignmentEditView(generic.ObjectEditView):
    queryset = models.AVPortAssignment.objects.all()
    form = forms.AVPortAssignmentForm


@register_model_view(models.AVPortAssignment, name="delete")
class AVPortAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = models.AVPortAssignment.objects.all()


@register_model_view(Device, "av")
class DeviceAVPortAssignmentsView(generic.ObjectChildrenView):
    queryset = Device.objects.all()
    child_model = models.AVPortAssignment
    table = tables.AVPortAssignmentTable
    tab = ViewTab(
        label="AV",
        badge=lambda obj: models.AVPortAssignment.objects.filter(
            Q(interface__device=obj) | Q(front_port__device=obj) | Q(rear_port__device=obj)
        ).count(),
        permission="netbox_av_plugin.view_avportassignment",
        weight=700,
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, "view").filter(
            Q(interface__device=parent) | Q(front_port__device=parent) | Q(rear_port__device=parent)
        )

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)
        table.columns.hide("device")
        return table
