# Generated by Django 5.0 on 2023-12-16 12:11

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_post_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='page',
            managers=[
                ('my_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]