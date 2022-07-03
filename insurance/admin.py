from django.contrib import admin
from insurance.models import Insurance, Procedure, Charge

# Register your models here.
class InsuranceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "insurance_name",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = ("insurance_name",)
    list_per_page = 50

class ProcedureAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "procedure_name",
        "billing_code",
        "revenue_code",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = ("procedure_name", "billing_code", "revenue_code",)
    list_per_page = 50

class ChargeAdmin(admin.ModelAdmin):

    list_display = (
        "id",

        "insurance",

        "procedure",
        "procedure_price",
        "hospital",

        "cash_price",
        "unit_price",

        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = ("procedure_price", "procedure_name", "hospital", "unit_price",)
    list_per_page = 50



admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(Procedure, ProcedureAdmin)
admin.site.register(Charge, ChargeAdmin)
