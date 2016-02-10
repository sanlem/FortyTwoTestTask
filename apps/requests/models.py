from django.db import models


class RequestEntry(models.Model):
    method = models.CharField(max_length=6)
    absolute_path = models.URLField()
    is_ajax = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ["-priority", "-timestamp"]
