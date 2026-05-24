"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path
from strawberry.django.views import GraphQLView

from config.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("_allauth/", include("allauth.headless.urls")),
    path("graphql/", GraphQLView.as_view(schema=schema)),
]
