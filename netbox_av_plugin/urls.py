from django.urls import include, path
from utilities.urls import get_model_urls

from . import views  # noqa: F401

urlpatterns = (
    path(
        "port-profiles/",
        include(get_model_urls("netbox_av_plugin", "avportprofile", detail=False)),
    ),
    path(
        "port-profiles/<int:pk>/",
        include(get_model_urls("netbox_av_plugin", "avportprofile")),
    ),
    path(
        "port-assignments/",
        include(get_model_urls("netbox_av_plugin", "avportassignment", detail=False)),
    ),
    path(
        "port-assignments/<int:pk>/",
        include(get_model_urls("netbox_av_plugin", "avportassignment")),
    ),
)
