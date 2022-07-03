from django.contrib import admin
from hospital.models import Specialization, Hospital

# Register your models here.
class SpecializationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = ("name",)
    list_per_page = 50



class HospitalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hospital_name",
        "specialization",
        "zip_code",
        "phone_no",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = ("hospital_name, specialization__name",)
    list_per_page = 50


admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Hospital, HospitalAdmin)
