# Generated by Django 4.2.5 on 2023-12-06 00:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import project.models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_alter_t8_sound_t6'),
    ]

    operations = [
        migrations.CreateModel(
            name='T5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(default='', null=True)),
                ('sound', models.FileField(null=True, upload_to=project.models.path_define, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav'])])),
                ('image1', models.ImageField(null=True, upload_to=project.models.path_define, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('image2', models.ImageField(null=True, upload_to=project.models.path_define, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('image3', models.ImageField(null=True, upload_to=project.models.path_define, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('image4', models.ImageField(null=True, upload_to=project.models.path_define, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])),
                ('answer', models.CharField(default='', max_length=20)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.lesson')),
            ],
        ),
    ]
