from rest_framework import serializers
from .models import Athlete, Reading, Alert

class ReadingInSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    timestamp_ms = serializers.IntegerField(required=False)
    timestamp_iso_utc = serializers.CharField(required=False)
    temperature_c = serializers.FloatField(required=False, allow_null=True)
    heart_rate_bpm = serializers.FloatField(required=False, allow_null=True)
    spo2_percent = serializers.FloatField(required=False, allow_null=True)
    signal_quality = serializers.IntegerField(required=False, default=0)
    wifi_connected = serializers.BooleanField(required=False)

class ReadingOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = "__all__"

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"
