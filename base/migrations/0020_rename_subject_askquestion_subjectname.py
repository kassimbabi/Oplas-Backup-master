# Generated by Django 5.1.4 on 2024-12-30 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_remove_comments_question_comments_content_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='askquestion',
            old_name='subject',
            new_name='SubjectName',
        ),
    ]
