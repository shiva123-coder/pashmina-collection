from django.shortcuts import get_object_or_404
from django.conf import settings
from product.models import Product, ProductImage

def basket_contents(request):
    basket_products = []
    total = 0
    product_count = 0

    basket = request.session.get('basket', {})

    for variation_key, item_data in basket.items():
        # Split the variation_key to get individual components
        product_id, selected_size, selected_color = variation_key.split('_')

        # Retrieve the product using the numerical product_id
        product = get_object_or_404(Product, pk=product_id)

        if isinstance(item_data, dict):
            quantity = item_data.get('quantity', 0)
            total += quantity * product.selling_price
            product_count += quantity

            # Access product images through the ProductImage model
            product_images = ProductImage.objects.filter(product=product, color=selected_color)
            image_url = product_images.first().image.url if product_images.exists() else None

            basket_products.append({
                'product_id': product_id,
                'quantity': quantity,
                'product': product,
                'selected_size': selected_size,
                'selected_color': selected_color,
                'image': image_url,
            })

    # Calculate total selling_price including any delivery charge and discount
    if total < settings.FREE_DELIVERY_OUTSET and basket_products:
        delivery_cost = 0
        free_delivery_eligibility = settings.FREE_DELIVERY_OUTSET - total
    else:
        delivery_cost = 0
        free_delivery_eligibility = 0

    sum_total = delivery_cost + total
    
    # Set the sum_total session variable
    request.session['sum_total'] = sum_total

    context = {
        'basket_products': basket_products,
        'total': total,
        'product_count': product_count,
        'delivery_cost': delivery_cost,
        'free_delivery_eligibility': free_delivery_eligibility,
        'free_delivery_outset': settings.FREE_DELIVERY_OUTSET,
        'sum_total': sum_total,
    }

    return context