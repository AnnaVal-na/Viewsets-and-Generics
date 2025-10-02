from django.contrib import admin
from django.urls import path, include, re_path
from .views import RootView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from myproject.health_views import HealthCheckView

schema_view = get_schema_view(
    openapi.Info(
        title="LMS API",
        default_version="v1",
        description="API for Learning Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@lms.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", RootView.as_view(), name="root"),
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("courses.urls")),
    # Документация
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("health/", HealthCheckView.as_view(), name="health_check"),
]
