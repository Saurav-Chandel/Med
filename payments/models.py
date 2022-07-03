from django.db import models
from user.models import User


# Create your models here.
class PaymentStripe(models.Model):

    payment_from = models.ForeignKey(to=User,on_delete=models.CASCADE, blank=True, null=True, related_name='stripe_payment_from')
    # todo: will remove
    payment_to = models.ForeignKey(to=User,on_delete=models.CASCADE, blank=True, null=True, related_name='stripe_payment_to')
    payment_details = models.JSONField(default=dict, blank=True, null=True)
    payment_status = models.CharField(max_length=64, blank=True, null=True)
    checkout_session_details = models.JSONField(default=dict, blank=True, null=True)
    portal_session_details = models.JSONField(default=dict, blank=True, null=True)
    checkout_session_id = models.CharField(default=None,max_length=128, blank=True, null=True)
    
    # todo: will remove
    stripe_product_id = models.CharField(max_length=200, null=True, blank=True)
    # todo: will remove
    stripe_customer_id = models.CharField(max_length=200, null=True, blank=True)

    # todo: will remove
    is_active = models.BooleanField(default=True)
    # todo: will remove
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id



class SubscriptionPlan(models.Model):

    plan_name = models.CharField(max_length=30, help_text="plan subscription name")
    plan_price = models.FloatField(default=0.0, help_text="plan price based on monthly subscription")
    # days = models.IntegerField(default=0)
    product_id = models.CharField(max_length=200, null=True, blank=True)
    price_id = models.CharField(max_length=200, null=True, blank=True)
    # is_active = models.BooleanField(default=True)
    # is_deleted = models.BooleanField(default=False)

    created_by = models.ForeignKey(to=User,on_delete=models.CASCADE,default=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "SubscriptionPlan"
