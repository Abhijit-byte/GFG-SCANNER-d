from django.urls import path
from . import views

app_name = 'scanner'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/scan/', views.scan_qr, name='scan_qr'),
]
