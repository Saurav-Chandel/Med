# Generated by Django 4.0 on 2022-01-06 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0005_alter_user_phone_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentStripe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_details', models.JSONField(default=dict)),
                ('payment_status', models.CharField(max_length=64, null=True)),
                ('checkout_session_details', models.JSONField(default=dict)),
                ('portal_session_details', models.JSONField(default=dict)),
                ('checkout_session_id', models.CharField(default=None, max_length=128, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stripe_payment_from', to='user.user')),
                ('payment_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stripe_payment_to', to='user.user')),
            ],
        ),
    ]