# Generated by Django 4.2.5 on 2023-12-06 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_t1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='for_task',
        ),
        migrations.AlterField(
            model_name='t1',
            name='task_name',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='t2',
            name='task_name',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='t3',
            name='task_name',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='t4',
            name='task_name',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='t5',
            name='task_name',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='t6',
            name='task_name',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='t7',
            name='task_name',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='t8',
            name='task_name',
            field=models.TextField(default='', null=True),
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
