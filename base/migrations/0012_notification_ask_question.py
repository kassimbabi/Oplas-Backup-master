# Generated by Django 5.1.2 on 2024-11-14 09:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_askquestion_class_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='ask_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='base.askquestion'),
        ),
    ]