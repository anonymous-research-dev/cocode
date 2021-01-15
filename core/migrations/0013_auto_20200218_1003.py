# Generated by Django 2.2.6 on 2020-02-18 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200217_1709'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='surveyanswer',
            unique_together={('course_id', 'material_id', 'question_id', 'user')},
        ),
        migrations.AddIndex(
            model_name='surveyanswer',
            index=models.Index(fields=['question_id'], name='core_survey_questio_3e714a_idx'),
        ),
    ]