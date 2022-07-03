# Generated by Django 4.0 on 2021-12-22 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='hospital',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='phone_no',
            field=models.CharField(blank=True, default=None, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='hospital',
            name='specialization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hospital.specialization'),
            preserve_default=False,
        ),
    ]
