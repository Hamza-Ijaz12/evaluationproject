# Generated by Django 4.2.5 on 2024-02-20 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_t6_audio5_t6_audio6'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t5',
            old_name='total_images',
            new_name='total_pairs',
        ),
    ]
