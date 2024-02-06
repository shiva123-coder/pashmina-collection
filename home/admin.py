from django.contrib import admin
from .models import OfferText, Cards, Carousel, TextOnHomepage


class ContactFormAdmin(admin.ModelAdmin):
    
    readonly_fields = (
        "first_name",
        "last_name",
        "email",
        "message",
       
    )

    fields = (
        "firs_tname",
        "last_name",
        "email",
        "message",
        
    )

    list_display = (
       "first_name",
       "last_name",
       "email",
       "message",

    )
    
    
admin.site.register(OfferText)
admin.site.register(Carousel)

admin.site.register(Cards)
admin.site.register(TextOnHomepage)

