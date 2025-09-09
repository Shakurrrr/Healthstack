from django.shortcuts import render
import datetime
import dateutil.parser
from django.utils.timezone import make_aware, is_naive
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from .models import Athlete, Reading, Alert
from .serializers import ReadingInSerializer, ReadingOutSerializer, AlertSerializer
from django.conf import settings

# Create your views here.


def parse_ts(ms=None, iso=None):
    if ms is not None:
        dt = datetime.datetime.utcfromtimestamp(ms/1000.0).replace(tzinfo=datetime.timezone.utc)
        return dt
    if iso:
        dt = dateutil.parser.isoparse(iso)
        if is_naive(dt):
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return dt.astimezone(datetime.timezone.utc)
    return datetime.datetime.now(datetime.timezone.utc)

class ReadingIngestViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]  # swap to IsAuthenticated for production

    def create(self, request):
        s = ReadingInSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        d = s.validated_data

        athlete, _ = Athlete.objects.get_or_create(
            external_id=d["external_id"],
            defaults={"name": d["external_id"]}
        )

        ts = parse_ts(d.get("timestamp_ms"), d.get("timestamp_iso_utc"))

        r = Reading.objects.create(
            athlete=athlete,
            timestamp=ts,
            temperature_c=d.get("temperature_c"),
            heart_rate_bpm=d.get("heart_rate_bpm"),
            spo2_percent=d.get("spo2_percent"),
            signal_quality=d.get("signal_quality", 0),
            raw_json=request.data
        )

        # Basic inline alerting (Celery version comes later)
        alerts = []
        hr_max = float(getattr(settings, "ALERT_HR_MAX", 180))
        spo2_min = float(getattr(settings, "ALERT_SPO2_MIN", 92))
        temp_max = float(getattr(settings, "ALERT_TEMP_MAX", 38.0))

        if r.heart_rate_bpm and r.heart_rate_bpm > hr_max:
            alerts.append(Alert.objects.create(athlete=athlete, level="crit", message=f"High HR: {r.heart_rate_bpm} bpm"))
        if r.spo2_percent and r.spo2_percent < spo2_min:
            alerts.append(Alert.objects.create(athlete=athlete, level="crit", message=f"Low SpO2: {r.spo2_percent}%"))
        if r.temperature_c and r.temperature_c > temp_max:
            alerts.append(Alert.objects.create(athlete=athlete, level="warn", message=f"High Temp: {r.temperature_c}°C"))

        return Response({
            "reading": ReadingOutSerializer(r).data,
            "alerts": AlertSerializer(alerts, many=True).data
        }, status=status.HTTP_201_CREATED)

class ReadingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ReadingOutSerializer
    permission_classes = [permissions.IsAuthenticated]  # protect UI/API
    def get_queryset(self):
        athlete_id = self.request.query_params.get("athlete")
        qs = Reading.objects.all()
        if athlete_id:
            qs = qs.filter(athlete__external_id=athlete_id)
        return qs[:2000]  # cap for UI

class AlertViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        athlete_id = self.request.query_params.get("athlete")
        qs = Alert.objects.all().order_by("-created_at")
        if athlete_id:
            qs = qs.filter(athlete__external_id=athlete_id)
        return qs[:1000]
