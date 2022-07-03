from django.contrib import admin
from review.models import Review
# Register your models here.
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "hospital",
        "procedure",
        "rating",
        "out_of_pocket_price",
        "hospital_price",
        "review",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    search_fields = ("review",)
    list_per_page = 50

admin.site.register(Review, ReviewAdmin)