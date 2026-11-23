from django.urls import path
from reports.views import health_check, ready_check

urlpatterns = [
    path('health', health_check, name='health_check'),
    path('ready', ready_check, name='ready_check'),
]
