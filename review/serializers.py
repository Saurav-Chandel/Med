from rest_framework import serializers
from hospital.serializers import *
from insurance.serializers import *
from .models import *
# from user.serializers import UserSerializer,MediaSerializer
from insurance.models import Procedure, Insurance
from hospital.models import Hospital

class ProcedureNameSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Procedure
        fields = ['procedure_name']

class HospitalNameSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Hospital
        fields = ['hospital_name']

class InsuranceNameSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Insurance
        fields = ['insurance_name']

class ReviewSerializer(serializers.ModelSerializer):
    procedure=ProcedureNameSerializer(read_only=True)
    hospital=HospitalNameSerializer(read_only=True)
    insurance=InsuranceNameSerializer(read_only=True)
    class Meta(object):
        model = Review
        fields = "__all__"