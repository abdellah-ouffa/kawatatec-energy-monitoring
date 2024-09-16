from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sensor
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
from .timescale_db import (
    insert_power_reading,
    get_latest_power_readings,
    create_power_readings_table,
)
import json
from django.utils import timezone


@login_required
def dashboard(request):
    sensors = Sensor.objects.all()
    return render(request, "power_optimization/dashboard.html", {"sensors": sensors})


@csrf_exempt
def add_power_reading(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sensor_id = data.get("sensor_id")
        current = data.get("current")

        if sensor_id is not None and current is not None:
            logger.info(f"Received data from sensor {sensor_id}: current = {current} A")
            insert_power_reading(sensor_id, timezone.now(), current)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(
                {"status": "error", "message": "Missing required data"}, status=400
            )
    return JsonResponse({"status": "error"}, status=400)


def get_power_readings(request):
    sensor_id = request.GET.get("sensor_id")
    limit = int(request.GET.get("limit", 100))
    readings = get_latest_power_readings(sensor_id, limit)
    return JsonResponse(readings, safe=False)


def initialize_db(request):
    create_power_readings_table()
    return JsonResponse({"status": "Database initialized"})
