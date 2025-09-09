from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Reading, Alert, Athlete

@shared_task
def scan_and_alert():
    hr_max = float(getattr(settings, "ALERT_HR_MAX", 180))
    spo2_min = float(getattr(settings, "ALERT_SPO2_MIN", 92))
    temp_max = float(getattr(settings, "ALERT_TEMP_MAX", 38.0))

    since = timezone.now() - timedelta(minutes=5)
    qs = Reading.objects.filter(timestamp__gte=since)
    for r in qs:
        if r.heart_rate_bpm and r.heart_rate_bpm > hr_max:
            Alert.objects.create(athlete=r.athlete, level="crit", message=f"High HR: {r.heart_rate_bpm} bpm")
        if r.spo2_percent and r.spo2_percent < spo2_min:
            Alert.objects.create(athlete=r.athlete, level="crit", message=f"Low SpO2: {r.spo2_percent}%")
        if r.temperature_c and r.temperature_c > temp_max:
            Alert.objects.create(athlete=r.athlete, level="warn", message=f"High Temp: {r.temperature_c}°C")
