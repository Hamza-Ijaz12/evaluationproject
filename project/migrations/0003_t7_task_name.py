# Generated by Django 4.2.5 on 2023-12-05 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_t7'),
    ]

    operations = [
        migrations.AddField(
            model_name='t7',
            name='task_name',
            field=models.CharField(default='', null=True),
        ),
    ]
