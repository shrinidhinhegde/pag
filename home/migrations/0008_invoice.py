# Generated by Django 3.0.8 on 2020-07-24 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200723_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=100, null=True)),
                ('issue_date', models.DateField(auto_now=True)),
                ('due_date', models.DateField(null=True)),
                ('paid', models.BooleanField(default=False)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Organisation')),
            ],
        ),
    ]
