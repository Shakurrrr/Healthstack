import json, os, signal, sys, time, datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
import paho.mqtt.client as mqtt
from vitals.models import Athlete, Reading

BROKER = os.getenv("MQTT_BROKER", "localhost")
TOPIC  = os.getenv("MQTT_TOPIC",  "athlete/data")
CLIENT = os.getenv("MQTT_CLIENT_ID", "healthstack-consumer")

stop = False

def _ts(payload):
    if "timestamp_ms" in payload:
        ms = int(payload["timestamp_ms"])
        return datetime.datetime.utcfromtimestamp(ms/1000.0).replace(tzinfo=datetime.timezone.utc)
    return datetime.datetime.now(datetime.timezone.utc)

def on_message(client, userdata, msg):
    try:
        p = json.loads(msg.payload.decode("utf-8"))
        ext = p.get("external_id") or "pi-001"
        athlete, _ = Athlete.objects.get_or_create(external_id=ext, defaults={"name": ext})

        Reading.objects.create(
            athlete=athlete,
            timestamp=_ts(p),
            temperature_c=p.get("temperature_c"),
            heart_rate_bpm=p.get("heart_rate_bpm"),
            spo2_percent=p.get("spo2_percent"),
            signal_quality=p.get("signal_quality", 0),
            raw_json=p
        )
    except Exception as e:
        print("MQTT consumer error:", e)

class Command(BaseCommand):
    help = "Run MQTT consumer that persists readings"

    def handle(self, *args, **kwargs):
        stop = False
        
        def _sig(*_):
            nonlocal stop
            stop = True

        signal.signal(signal.SIGINT, _sig)
        signal.signal(signal.SIGTERM, _sig)

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT)
        client.on_message = on_message
        client.connect(BROKER, 1883, keepalive=30)
        client.subscribe(TOPIC, qos=0)
        client.loop_start()
        self.stdout.write(self.style.SUCCESS(f"MQTT consumer connected to {BROKER}, topic {TOPIC}"))
        while not stop:
            time.sleep(0.5)
        client.loop_stop()
        client.disconnect()
