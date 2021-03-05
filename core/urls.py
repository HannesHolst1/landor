# -*- encoding: utf-8 -*-


from django import urls
from django.contrib import admin
from django.urls import path, include  # add this

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("grapesjs.urls")),
    path("", include("app.urls"))             # UI Kits Html files
]