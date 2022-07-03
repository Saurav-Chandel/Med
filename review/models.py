from django.db import models
from django.core.validators import MaxValueValidator
from hospital.models import Hospital
from insurance.models import Charge, Procedure, Insurance
from user.models import User
from user.models import Media

# Create your models here.
class Review(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="review_hospital")
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="review_procedure")
    insurance = models.ForeignKey(Insurance, blank=True, null=True, on_delete=models.CASCADE, related_name="review_insurance")
    rating = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)
    out_of_pocket_price = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)
    hospital_price = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)
    review = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_field= models.FileField(upload_to="review_file/", blank=True, null=True)

    def __str__(self):
        return str(self.id)