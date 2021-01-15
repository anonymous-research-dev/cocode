from datetime import datetime, timedelta
from .time_stamped_model import TimeStampedModel
from django.db import models

class ExerciseLogBundle(TimeStampedModel):
    course_id = models.SlugField()
    material_id = models.SlugField()
    logs = models.TextField(blank=True, default='[]')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['course_id']),
            models.Index(fields=['material_id']),
            models.Index(fields=['user']),
        ]
