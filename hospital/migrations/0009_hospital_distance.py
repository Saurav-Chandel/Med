# Generated by Django 4.0 on 2022-01-04 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0008_alter_hospital_specialization'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='distance',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]