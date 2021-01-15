from datetime import datetime
from .time_stamped_model import TimeStampedModel
from django.db import models


class CourseState(TimeStampedModel):
    course_id = models.SlugField()
    exp_group_id = models.CharField(max_length=64, blank=True, default='')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course_id', 'user',)
        indexes = [
            models.Index(fields=['course_id']),
            models.Index(fields=['user']),
        ]

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'exp_group_id': self.exp_group_id,
            'user_id': self.user_id,
            'created_at': datetime.timestamp(self.created_at),
            'updated_at': datetime.timestamp(self.updated_at),
        }
