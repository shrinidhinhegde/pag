# Generated by Django 3.0.8 on 2020-07-24 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='Documents'),
        ),
    ]