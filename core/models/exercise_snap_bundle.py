import json
import random
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from .time_stamped_model import TimeStampedModel
from .exercise_state import ExerciseState
from .material_state import MaterialState
from .user import User
from django.db import models
from django.db.models import Count
from django.utils import timezone


class ExerciseSnapBundle(TimeStampedModel):
    course_id = models.SlugField()
    material_id = models.SlugField()
    snaps = models.TextField(blank=True, default='[]')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['course_id']),
            models.Index(fields=['material_id']),
            models.Index(fields=['user']),
        ]

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'material_id': self.material_id,
            'snaps': json.loads(self.snaps),
            'created_at': datetime.timestamp(self.created_at),
            'updated_at': datetime.timestamp(self.updated_at),
        }

    @staticmethod
    def get_user_snaps_dict(course_id, material_id, user_count=20):
        # Get users who completed the exercise.
        user_ids = MaterialState.objects\
            .values('user_id')\
            .filter(
                course_id=course_id,
                material_id=material_id, 
                progress__gte=100, 
                star__gte=1,
            )\
            .order_by('?')
        if len(user_ids) > user_count:
            user_ids = [row['user_id'] for row in user_ids[:20]]

        users = User.objects.filter(id__in=user_ids)
        user_dict = {}
        for user in users:
            user_dict[user.id] = user
        
        # Get all snaps from these users.
        bundles = ExerciseSnapBundle.objects \
            .filter(
                course_id=course_id,
                material_id=material_id,
                user_id__in=user_ids,
            )\
            .order_by('user_id', 'created_at')

        user_snaps_dict = defaultdict(list)
        for bundle in bundles:
            username = bundle.user.username
            bundle_snaps = json.loads(bundle.snaps)
            for snap in bundle_snaps:
                user_snaps_dict[username].append(snap)
        
        return user_snaps_dict

    # @staticmethod
    # def get_snaps_to_play(course_id, material_id):
    #     duration_date = 30
    #     user_count = 20
    #     slot_length_mins = 20
    #     top_slot_count = 10 

    #     datetime_now = datetime.now(tz=timezone.utc)
    #     duration_delta = timedelta(days=duration_date)
    #     busy_users = ExerciseSnapBundle.objects \
    #         .filter(
    #             course_id=course_id,
    #             material_id=material_id,
    #             created_at__gte=(datetime_now - duration_delta),
    #             created_at__lt=datetime_now,
    #         ) \
    #         .values('user_id') \
    #         .annotate(count=Count('user_id')) \
    #         .filter(count__gt=1) \
    #         .order_by('-count')
            
    #     if len(busy_users) == 0:
    #         # No users to replay.
    #         return []

    #     if len(busy_users) > user_count:
    #         busy_users = busy_users[:user_count]

    #     def get_ts_id(x):
    #         return datetime.timestamp(
    #             x['created_at']) // (slot_length_mins * 60)
    #     stamped_snaps = []
    #     slot_length_delta = timedelta(minutes=slot_length_mins)
    #     for busy_user in busy_users:
    #         user_id = busy_user['user_id']
    #         snap_datetimes = ExerciseSnapBundle.objects \
    #             .filter(
    #                 course_id=course_id,
    #                 material_id=material_id,
    #                 created_at__gte=(datetime_now - duration_delta),
    #                 created_at__lt=datetime_now,
    #                 user_id=user_id,
    #             ) \
    #             .values('created_at')
    #         snap_ts_ids = [get_ts_id(m) for m in snap_datetimes]
    #         ts_ids_counter = Counter(snap_ts_ids)

    #         most_common_ids = [ts_id for ts_id, count in ts_ids_counter.most_common(
    #             top_slot_count) if count > 0]
    #         random.shuffle(most_common_ids)
    #         max_ts_id = most_common_ids[0]

    #         start_timestamp = max_ts_id * slot_length_mins * 60
    #         start_datetime = datetime.fromtimestamp(
    #             start_timestamp, tz=timezone.utc)
    #         snap_bundles = ExerciseSnapBundle.objects \
    #             .filter(
    #                 course_id=course_id,
    #                 material_id=material_id,
    #                 created_at__gte=start_datetime,
    #                 created_at__lt=(start_datetime + slot_length_delta),
    #                 user_id=user_id,
    #             )
    #         for snap_bundle in snap_bundles:
    #             curr_snaps = json.loads(snap_bundle.snaps)
    #             for snap in curr_snaps:
    #                 stamped_snaps.append([
    #                     snap['ts'] - (start_timestamp * 1000),
    #                     snap_bundle.user.username,
    #                     snap
    #                 ])
    #     stamped_snaps.sort()
    #     return stamped_snaps
            




