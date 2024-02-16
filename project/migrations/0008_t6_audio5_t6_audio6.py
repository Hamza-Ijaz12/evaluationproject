# Generated by Django 4.2.5 on 2024-02-16 17:45

import django.core.validators
from django.db import migrations, models
import project.models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_rename_sound_t5_sound1_t5_image5_t5_image6_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='t6',
            name='audio5',
            field=models.FileField(blank=True, null=True, upload_to=project.models.path_define, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav'])]),
        ),
        migrations.AddField(
            model_name='t6',
            name='audio6',
            field=models.FileField(blank=True, null=True, upload_to=project.models.path_define, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav'])]),
        ),
    ]
