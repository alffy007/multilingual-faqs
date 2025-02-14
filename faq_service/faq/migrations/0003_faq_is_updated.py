# Generated by Django 5.1.5 on 2025-02-01 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_remove_faq_answer_remove_faq_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='is_updated',
            field=models.BooleanField(default=False, help_text='Flag indicating if the FAQ content has been updated'),
        ),
    ]
