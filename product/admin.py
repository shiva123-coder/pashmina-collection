from django.contrib import admin
from .models import Category, ProductImage, WomanProduct, ManProduct, UnisexProduct, Variation, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'display_name')
    prepopulated_fields = {'slug': ('category_name',)}

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'color')  # Include 'color' field

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, VariationInline]
    list_display = ('product_name', 'selling_price', 'old_price', 'category', 'modified_date', 'is_available')
    list_filter = ('category', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

    def save_model(self, request, obj, form, change):
        # Save the main product instance
        super().save_model(request, obj, form, change)

        # Save images with the corresponding product and color
        for color in form.cleaned_data.get('colors', []):
            image = ProductImage(product=obj, color=color, image=form.cleaned_data['image'])
            image.save()

admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)
admin.site.register(WomanProduct, ProductAdmin)
admin.site.register(ManProduct, ProductAdmin)
admin.site.register(UnisexProduct, ProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
