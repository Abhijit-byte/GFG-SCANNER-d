from django.urls import path
from .views import scan_qr, scanner_page

urlpatterns = [
    path("", scanner_page),      # opens scanner
    path("scan/", scan_qr),      # API endpoint
]
