from django.shortcuts import (
    render, redirect, get_object_or_404, reverse, HttpResponse)
from product.models import Product, Variation
from django.contrib import messages
from django.conf import settings
from django.db.models import F
from django.db import transaction

# Create your views here.
def view_basket(request):
    """ render the shopping basket page """
    return render(request, 'basket/basket.html')


def reset_inactivity_timer(request):
    """Reset the inactivity timer"""
    request.session['basket_timer_reset'] = True
    

def add_to_basket(request, product_id):
    """Add product details, including color, size, and quantity, to the basket"""
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    selected_size = request.POST.get('size')
    selected_color = request.POST.get('color')
    
    # Change the way you construct the variation key
    variation_key = f"{product_id}_{selected_size}_{selected_color}"

    # Check if the variation exists
    variation = get_object_or_404(Variation, product=product, size=selected_size, color=selected_color)

    # Check if the requested quantity is available in stock
    if variation.stock_quantity >= quantity:
        basket = request.session.get('basket', {})

        if variation_key in basket:
            basket[variation_key]['quantity'] += quantity
        else:
            basket[variation_key] = {
                'product_id': product_id,
                'product_name': product.product_name,
                'selling_price': product.selling_price,
                'selected_size': selected_size,
                'selected_color': selected_color,
                'quantity': quantity,
            }

        # Update the stock quantity after adding to the basket
        variation.stock_quantity = F('stock_quantity') - quantity
        variation.save()

        request.session['basket'] = basket
        messages.success(request, f"{product.product_name} has been added to your basket.")
        
        # Call the resetInactivityTimer function after adding the item to the basket
        reset_inactivity_timer(request)
        
    else:
        messages.error(request, f"Sorry, we only have only {variation.stock_quantity} stock for {product.product_name} with the selected size and color, please ammend the quantity or choose another variation")
        return redirect(reverse('product_details', args=[product_id]))
    
    request.session['basket_item_added'] = True
    return redirect(reverse('all_products'))



def update_basket(request, product_id):
    """Update the quantity of a product in the basket"""
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    selected_size = request.POST.get('size')
    selected_color = request.POST.get('color')

    variation_key = f"{product_id}_{selected_size}_{selected_color}"

    basket = request.session.get('basket', {})

    if variation_key in basket:
        variation = Variation.objects.get(product=product, size=selected_size, color=selected_color)

        # Calculate the difference in quantity
        diff_quantity = quantity - basket[variation_key]['quantity']

        if quantity <= variation.stock_quantity + basket[variation_key]['quantity']:
            # Update the quantity in the session
            basket[variation_key]['quantity'] = quantity
            request.session['basket'] = basket

            # Update the stock quantity in the database
            with transaction.atomic():
                variation.stock_quantity = F('stock_quantity') - diff_quantity
                variation.save()

            messages.success(request, f"{product.product_name} quantity has been updated.")
            
            # Call the resetInactivityTimer function after updating the basket
            reset_inactivity_timer(request)
            
        else:
            messages.error(request, f"Sorry, we only have only {variation.stock_quantity} stock for {product.product_name} with the selected size and color, please ammend the quantity or choose another variation")
            return redirect('view_basket')
    else:
        messages.error(request, f"Error updating quantity for {product.product_name} in the basket.")
        
    request.session['basket_updated'] = True
    return redirect('view_basket')


def remove_basket(request, product_id):
    """Remove a product from the basket"""
    product = get_object_or_404(Product, pk=product_id)

    # Retrieve size and color from the request
    selected_size = request.POST.get('size')
    selected_color = request.POST.get('color')

    # Construct the variation_key based on product_id, size, and color
    variation_key = f"{product_id}_{selected_size}_{selected_color}"

    basket = request.session.get('basket', {})

    if variation_key in basket:
        # Retrieve the quantity from the basket
        quantity = basket[variation_key]['quantity']
        
        # Call the increase_stock method to update the stock quantity (refer to models.py to find out about this method)
        variation = Variation.objects.get(product=product, size=selected_size, color=selected_color)
        variation.increase_stock(quantity)
        
        # Remove the item from the basket
        del basket[variation_key]
        request.session['basket'] = basket
        messages.success(request, f"{product.product_name} has been removed from the basket.")
        
        # Call the resetInactivityTimer function after removing item the basket
        reset_inactivity_timer(request)
    else:
        messages.error(request, f"Error removing {product.product_name} from the basket.")

    return redirect(reverse('view_basket'))


## View to remove entire basket when user is inactive for certain period of time
## refer to bottom of the base.html page to understand javascript logic to deal with time and basket removal
def remove_whole_basket(request):
    if 'basket' in request.session:
        basket = request.session.pop('basket', {})  # Remove basket from session and get its contents
        for item_key, item_data in basket.items():
            product_id, size, color = item_key.split('_')
            quantity = item_data['quantity']
            
            # Increase the stock quantity for the item back to the inventory
            variation = Variation.objects.get(product_id=product_id, size=size, color=color)
            variation.stock_quantity += quantity
            variation.save()
        
        messages.info(request, "Your basket is emptied due to inactivity. Please re-add your favorites")
    return redirect('view_basket')