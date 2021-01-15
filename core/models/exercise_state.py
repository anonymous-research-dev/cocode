import json
from datetime import datetime
from .time_stamped_model import TimeStampedModel
from django.db import models
from django.dispatch import receiver
from django.db.models import signals
from core.utils.courses import load_exercise_files_dict

class ExerciseState(TimeStampedModel):
    course_id = models.SlugField()
    material_id = models.SlugField()
    value = models.TextField(blank=True)
    edit_seconds = models.PositiveIntegerField(default=0)
    open_seconds = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course_id', 'material_id', 'user',)
        indexes = [
            models.Index(fields=['course_id']),
            models.Index(fields=['material_id']),
            models.Index(fields=['user']),
        ]

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'material_id': self.material_id,
            'value': json.loads(self.value),
            'edit_seconds': self.edit_seconds,
            'open_seconds': self.open_seconds,
            'created_at': datetime.timestamp(self.created_at),
            'updated_at': datetime.timestamp(self.updated_at),
        }

    def get_seconds_dict(self):
        return {
            'edit_seconds': self.edit_seconds,
            'open_seconds': self.open_seconds,
        }

    def set_default_value(self):
        tree = load_exercise_files_dict(self.course_id, self.material_id)
        self.value = json.dumps(tree)
        self.save()


@receiver(signals.post_save, sender=ExerciseState)
def load_default_value(sender, instance, created, **kwargs):
    if created:
        instance.set_default_value()
