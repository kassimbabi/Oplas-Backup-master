# Generated by Django 5.1.4 on 2024-12-29 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_webimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='askquestion',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]