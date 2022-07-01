# Generated by Django 3.2.7 on 2022-07-01 15:30

import courses.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_content_file_image_text_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='photo',
            field=models.ImageField(blank=True, default=courses.models.get_default_image, null=True, upload_to=courses.models.get_course_image_filepath),
        ),
    ]
