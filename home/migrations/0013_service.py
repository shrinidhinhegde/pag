# Generated by Django 3.0.8 on 2020-07-28 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_renewal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_service', models.CharField(blank=True, max_length=500, null=True)),
                ('start_of_service', models.DateField(null=True)),
                ('end_of_service', models.DateField(null=True)),
                ('product', models.CharField(blank=True, max_length=500, null=True)),
                ('jurisdiction', models.CharField(blank=True, max_length=200, null=True)),
                ('cancel_status', models.BooleanField(default=False)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Organisation')),
            ],
        ),
    ]
