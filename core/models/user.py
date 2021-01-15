import random
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_restricted = models.BooleanField(default=False)
    is_temporary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['username']),
        ]

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_restricted': self.is_restricted,
            'is_temporary': self.is_temporary,
            'is_active': self.is_active,
        }

    @staticmethod
    def create_experiment_user():
        def get_random_string(length):
            return ''.join(random.choice('abcedfghijklmnopqrstuvwxyz0123456789') for i in range(length))
        password = get_random_string(16)
        while True:
            username = 'exp__%s' % get_random_string(16)
            try:
                _ = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(
                    username=username,
                    password=password,
                    is_restricted=True,
                )
                user.save()
                return user
