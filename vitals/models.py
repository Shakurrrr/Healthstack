from django.db import models

# Create your models here.

class Athlete(models.Model):
    name = models.CharField(max_length=120)
    external_id = models.CharField(max_length=120, unique=True)  # map device/user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.external_id})"


class Reading(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="readings")
    timestamp = models.DateTimeField(db_index=True)
    temperature_c = models.FloatField(null=True, blank=True)
    heart_rate_bpm = models.FloatField(null=True, blank=True)
    spo2_percent = models.FloatField(null=True, blank=True)
    signal_quality = models.IntegerField(default=0)
    raw_json = models.JSONField(default=dict, blank=True)  # keep original payload for audit

    class Meta:
        indexes = [
            models.Index(fields=["athlete", "timestamp"]),
        ]
        ordering = ["-timestamp"]


class Alert(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="alerts")
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=16, choices=[("info","info"),("warn","warn"),("crit","crit")], default="warn")
    message = models.TextField()
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.level}] {self.athlete} {self.created_at:%Y-%m-%d %H:%M}"
