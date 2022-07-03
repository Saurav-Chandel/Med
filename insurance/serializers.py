from rest_framework import serializers
from .models import *
from hospital.serializers import *
from user.serializers import UserSerializer
from review.models import Review
from django.db.models import Avg

class InsuranceSerializer(serializers.ModelSerializer):
    created_by=UserSerializer(read_only=True)
    class Meta:
        model = Insurance
        fields = "__all__"

class CreateInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = "__all__"        


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = "__all__"


class CreateChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = "__all__"


class ChargeSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField(method_name='get_review')

    hospital=HospitalSerializer(read_only=True)
    procedure=ProcedureSerializer(read_only=True)
    insurance=InsuranceSerializer(read_only=True)
    class Meta:
        model = Charge
        fields = "__all__"

    def get_review(self,obj):
        queryset=Review.objects.filter(hospital=obj.hospital_id).aggregate(Avg('rating'))
        return queryset
        

class CreateUserInsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInsurance
        fields = "__all__"


class UserInsuranceSerializer(serializers.ModelSerializer):
    insurance=InsuranceSerializer(read_only=True)

    class Meta:
        model = UserInsurance
        fields = "__all__"