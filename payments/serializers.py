from rest_framework import serializers
from .models import *
from django.db.models import Avg


class PaymentStripeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStripe
        fields = "__all__"