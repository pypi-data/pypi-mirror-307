from django.db import models

class Task(models.Model):
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=255, null=True, blank=True)
  pid = models.IntegerField(null=True, blank=True)
  progress_percentage = models.IntegerField(default=0)
  start_date_time = models.DateTimeField(auto_now_add=True)
  end_date_time = models.DateTimeField(null=True, blank=True)
  input = models.JSONField(null=True, blank=True)
  output = models.JSONField(null=True, blank=True)

  class Meta:
    db_table = "lilota_store"