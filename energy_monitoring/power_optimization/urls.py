from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="power_dashboard"),
    path("add_reading/", views.add_power_reading, name="add_power_reading"),
    path("get_readings/", views.get_power_readings, name="get_power_readings"),
    path("initialize_db/", views.initialize_db, name="initialize_db"),
]
