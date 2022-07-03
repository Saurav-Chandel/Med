# Generated by Django 4.0 on 2021-12-23 07:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insurance', '0006_charge_created_by_insurance_created_by_and_more'),
        ('hospital', '0004_hospital_created_by_specialization_created_by'),
        ('user', '0003_alter_user_managers_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveBigIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999999)])),
                ('out_of_pocket_price', models.PositiveBigIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999999)])),
                ('hospital_price', models.PositiveBigIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999999)])),
                ('review', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_hospital', to='hospital.hospital')),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_procedure', to='insurance.procedure')),
            ],
        ),
    ]
