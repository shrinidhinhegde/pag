# Generated by Django 3.0.8 on 2020-07-28 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_invoice_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Renewal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('received_date', models.DateField(auto_now=True)),
                ('due_date', models.DateField(null=True)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Organisation')),
            ],
        ),
    ]