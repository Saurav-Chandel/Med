from django.db import models
from django.core.validators import MaxValueValidator
from app.choices import *
from user.models import User

# Create your models here.
class Specialization(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    hospital_name = models.CharField(
        max_length=250, default=None, null=True, blank=True
    )
    distance=models.IntegerField(blank=True,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    # rating = models.PositiveBigIntegerField(
    #     validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE,related_name='hospital_specialization')
    info = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    zip_code = models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)], blank=True, null=True)
    phone_no = models.CharField(
        max_length=12, default=None, null=True, blank=True
    )
    hospital_image = models.FileField(upload_to="hospital_image/", blank=True, null=True)


    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hospital_name