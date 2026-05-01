from netbox.api.routers import NetBoxRouter

from . import views

app_name = "netbox_av_plugin"

router = NetBoxRouter()
router.register("port-profiles", views.AVPortProfileViewSet)
router.register("port-assignments", views.AVPortAssignmentViewSet)

urlpatterns = router.urls
