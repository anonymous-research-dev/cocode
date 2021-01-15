from datetime import datetime
from .time_stamped_model import TimeStampedModel
from django.db import models


class SurveyAnswer(TimeStampedModel):
    course_id = models.SlugField()
    material_id = models.SlugField()
    question_id = models.SlugField()
    value = models.TextField(blank=True, default='')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course_id', 'material_id', 'question_id', 'user',)
        indexes = [
            models.Index(fields=['course_id']),
            models.Index(fields=['material_id']),
            models.Index(fields=['question_id']),
            models.Index(fields=['user']),
        ]

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'material_id': self.material_id,
            'question_id': self.question_id,
            'value': self.value,
            'created_at': datetime.timestamp(self.created_at),
            'updated_at': datetime.timestamp(self.updated_at),
        }
