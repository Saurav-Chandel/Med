from django.db import models
from django.core.validators import MaxValueValidator
from hospital.models import Hospital
from user.models import User

# Create your models here.
class Insurance(models.Model):
    insurance_name = models.CharField(
        max_length=250, default=None, null=False, blank=False
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.insurance_name

class Procedure(models.Model):
    procedure_name = models.CharField(
        max_length=250, default=None, null=False, blank=False
    )
    billing_code = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)
    revenue_code = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.procedure_name

class Charge(models.Model):
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name="insurance")
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="procedure")
    procedure_price = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="hospital")    
    cash_price = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)

    unit_price = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)
    maximum_negotiated_price= models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)
    minimum_negotiated_price= models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price=models.PositiveBigIntegerField(
        validators=[MaxValueValidator(9999999)], blank=True, null=True, unique=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.price = self.unit_price -self.procedure_price
        super(Charge, self).save(*args, **kwargs) # Call the "real" save() method.  



class UserInsurance(models.Model):
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name="user_insurance")

    group_number = models.CharField(
        max_length=250, default=None, null=False, blank=False
    )
    member_id = models.CharField(
        max_length=250, default=None, null=False, blank=False
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)