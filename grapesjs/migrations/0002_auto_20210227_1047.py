# Generated by Django 3.1.7 on 2021-02-27 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grapesjs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_content',
            name='css',
        ),
        migrations.RemoveField(
            model_name='user_content',
            name='html',
        ),
    ]
