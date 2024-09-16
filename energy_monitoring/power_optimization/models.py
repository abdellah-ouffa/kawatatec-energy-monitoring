from django.db import models
from django.contrib.auth.models import User


class Sensor(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    sensor_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.sensor_type})"


class PowerReading(models.Model):
    time = models.DateTimeField(primary_key=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    energy = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["sensor", "time"]),
        ]
