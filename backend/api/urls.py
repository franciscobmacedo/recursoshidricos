from django.urls import path

from api.views import api
from django.views.generic.base import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url="latest/")),
    path("latest/", RedirectView.as_view(url="v1/")),
    path("v1/", api.urls),
]
