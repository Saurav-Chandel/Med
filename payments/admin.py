from django.contrib import admin
from payments.models import PaymentStripe, SubscriptionPlan
from django.conf import settings
# import stripe

# stripe.api_key = getattr(settings,'STRIPE_API_KEY')

# Register your models here.
class PaymentStripeAdmin(admin.ModelAdmin):
    list_display = (
        "id",

        "payment_from",

        "is_active",
        "is_deleted",

        "payment_status",

        "created_at",
        "updated_at",
    )
    list_display_links = ("id",)
    list_per_page = 50
    search_fields = ('payment_from__email', 'payment_status',)

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        "id",

        "plan_name",

        "plan_price",
        "product_id",
        "price_id",

        "created_at",
        "updated_at",
    )

    readonly_fields = ('product_id', "price_id")

    def save_model(self, request, obj, form, change):


        if change == True:
            try:
                stripe.Product.modify(str(obj.product_id),
                    name=str(form.cleaned_data['plan_name'])
                )

                # TODO: this is not working
                z = stripe.Plan.modify(str(obj.price_id), 
                    amount=int(form.cleaned_data['plan_price'])
                )
                print(z)
            except Exception as e:
                print(e)


        # TODO: stripe subscription plan crud
        if change == False:
            product_id = stripe.Product.create(name=form.cleaned_data['plan_name']).id
            obj.product_id = product_id
            price_id = stripe.Plan.create(amount=int(form.cleaned_data['plan_price']),currency="usd",interval="month",product=str(product_id),).id
            obj.price_id = price_id
            
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        print(obj.price_id)
        print(obj.product_id)


        try:
            stripe.Plan.delete(str(obj.price_id),)
            stripe.Product.delete(str(obj.product_id),)
        except Exception as e:
            print(e)
        
        """
        you can do anything here BEFORE deleting the object
        """

        obj.delete()




admin.site.register(PaymentStripe, PaymentStripeAdmin)