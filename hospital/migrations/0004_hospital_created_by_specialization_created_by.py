# Generated by Django 4.0 on 2021-12-23 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_managers_token'),
        ('hospital', '0003_hospital_created_at_hospital_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
        migrations.AddField(
            model_name='specialization',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user'),
        ),
    ]