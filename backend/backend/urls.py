from django.contrib import admin
from django.urls import path, include

from api.views import api

urlpatterns = []
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
