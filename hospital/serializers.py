from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer
# from review.serializers import CreateReviewSerializer
from django.db.models import Avg
from review.models import Review

class CreateHospitalSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Hospital
        fields = "__all__"

class SpecializationSerializer(serializers.ModelSerializer):
    # hospital_specialization=CreateHospitalSerializer(many=True)
    class Meta(object):
        model = Specialization
        fields = ("id","name")

class HospitalSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField(method_name='get_review')

    # review_hospital=CreateReviewSerializer(many=True)
    specialization=SpecializationSerializer(read_only=True)
    # created_by=UserSerializer(read_only=True)
    class Meta(object):
        model = Hospital
        fields = "__all__"

    def get_review(self,obj):
        print(obj)
        queryset=Review.objects.filter(hospital=obj.id).aggregate(Avg('rating'))
        print(queryset)
        return queryset
        