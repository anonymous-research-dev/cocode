from datetime import datetime
from django.db import models
from .time_stamped_model import TimeStampedModel


class MaterialState(TimeStampedModel):
    course_id = models.SlugField()
    material_id = models.SlugField()
    progress = models.PositiveSmallIntegerField(default=0)
    star = models.PositiveSmallIntegerField(default=0)
    value = models.TextField(blank=True, default='')
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
            'progress': self.progress,
            'star': self.star,
            'value': self.value,
            'created_at': datetime.timestamp(self.created_at),
            'updated_at': datetime.timestamp(self.updated_at),
        }
