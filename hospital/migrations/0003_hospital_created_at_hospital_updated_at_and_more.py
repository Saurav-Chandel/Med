# Generated by Django 4.0 on 2021-12-22 10:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_specialization_hospital_address_hospital_info_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='specialization',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specialization',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
