from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("scanner.urls")),   # 👈 ROOT now opens scanner
    path("admin/", admin.site.urls),
    path("api/", include("scanner.urls")),  # API still works
]
