# Generated by Django 3.0.8 on 2020-08-20 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20200820_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='suborganisation',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
