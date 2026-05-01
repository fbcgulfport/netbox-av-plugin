from django.db.models import Count
from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import AVPortAssignmentSerializer, AVPortProfileSerializer


class AVPortProfileViewSet(NetBoxModelViewSet):
    queryset = models.AVPortProfile.objects.annotate(assignment_count=Count("assignments")).prefetch_related("tags")
    serializer_class = AVPortProfileSerializer
    filterset_class = filtersets.AVPortProfileFilterSet


class AVPortAssignmentViewSet(NetBoxModelViewSet):
    queryset = models.AVPortAssignment.objects.select_related(
        "profile",
        "interface__device",
        "front_port__device",
        "rear_port__device",
    ).prefetch_related("tags")
    serializer_class = AVPortAssignmentSerializer
    filterset_class = filtersets.AVPortAssignmentFilterSet
