from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import(
    Category, Product, WomanProduct, ManProduct, UnisexProduct, Variation)
from django.http import JsonResponse

from .forms import ProductForm

# View for all products
def all_products(request):
    products = Product.objects.filter(is_available=True).order_by('product_name')
    categories = Category.objects.all()  # Retrieve all categories to display in filters
    
    query = request.GET.get('q')
    
    if query:
        products = products.filter(Q(product_name__icontains=query) | Q(description__icontains=query))
    
    context = {
       'products': products,
       'categories': categories,
       'query': query,
    }
    return render(request, 'product/product.html', context)

# View to display product details
def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variations = product.variation_set.all()
    
    images = []
    for variation in variations:
        # Assuming each variation has a related product image
        variation_images = variation.productimage_set.all()
        if variation_images:
            images.extend(variation_images)
    
    context = {
        'product': product,
        'images': images,
        'variations': variations,
    }
    return render(request, 'product/product_details.html', context)



# View for Woman products
def woman_products(request):
    womanproducts = WomanProduct.objects.filter(is_available=True).order_by('product_name')
    query = None
    categories = None
    sort = None
    direction = None
    image = None
    
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            if sortkey == "product_name":
                womanproducts = womanproducts.annotate(sortkey=Lower("product_name"))

            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == 'desc':
                    sortkey = f"-{'price'}"
                    if sortkey == "None":
                        womanproducts = womanproducts
                    else:
                        womanproducts = womanproducts.order_by(sortkey)
                else:
                    direction == 'asc'
                    sortkey = f"{'price'}"
                    if sortkey == "None":
                        womanproducts = womanproducts
                    else:
                        womanproducts = womanproducts.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            womanproducts = womanproducts.filter(category__category_name__in=categories)
            categories = Category.objects.filter(category_name__in=categories)

        if 'q1' in request.GET:
            query = request.GET['q1']
            if not query:
                messages.error(request, "No search criteria entered!")
                return redirect(reverse('womanproducts'))
            queries = Q(product_name__icontains=query) | Q(description__icontains=query)
            womanproducts = womanproducts.filter(queries)

    existing_sorting = f'{sort}_{direction}'

    context = {
        'womanproducts': womanproducts,
        'search_term': query,
        'existing_categories': categories,
        'existing_sorting': existing_sorting,
        'image': image,
    }
    return render(request, 'product/woman_product.html', context)


# View for Man products
def man_products(request):
    manproducts = ManProduct.objects.filter(is_available=True).order_by('product_name')
    query = None
    categories = None
    sort = None
    direction = None
    image = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            if sortkey == "product_name":
                manproducts = manproducts.annotate(sortkey=Lower("product_name"))

            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == 'desc':
                    sortkey = f"-{'price'}"
                    if sortkey == "None":
                        manproducts = manproducts
                    else:
                        manproducts = manproducts.order_by(sortkey)
                else:
                    direction == 'asc'
                    sortkey = f"{'price'}"
                    if sortkey == "None":
                        manproducts = manproducts
                    else:
                        manproducts = manproducts.order_by(sortkey)
                        
                        

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            manproducts = manproducts.filter(category__category_name__in=categories)
            categories = Category.objects.filter(category_name__in=categories)

        if request.GET:
            if 'q1' in request.GET:
                query = request.GET['q1']
                if not query:
                    messages.error(request, "No search criteria entered!")
                    return redirect(reverse('manproducts'))
                queries = Q(product_name__icontains=query) | Q(
                    description__icontains=query)
                manproducts = manproducts.filter(queries)                   
                   
                
    existing_sorting = f'{sort}_{direction}'

    context = {
        'manproducts': manproducts,
        'search_term': query,
        'existing_categories': categories,
        'existing_sorting': existing_sorting,
        'image': image,

    }
    return render(request, 'product/man_product.html', context)

# View for Kids products
def unisex_products(request):
    unisexproducts = UnisexProduct.objects.filter(is_available=True).order_by('product_name')
    query = None
    categories = None
    sort = None
    direction = None
    image = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            if sortkey == "product_name":
                unisexproducts = unisexproducts.annotate(sortkey=Lower("product_name"))

            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == 'desc':
                    sortkey = f"-{'price'}"
                    if sortkey == "None":
                        unisexproducts = unisexproducts
                    else:
                        unisexproducts = unisexproducts.order_by(sortkey)
                else:
                    direction == 'asc'
                    sortkey = f"{'price'}"
                    if sortkey == "None":
                        unisexproducts = unisexproducts
                    else:
                        unisexproducts = unisexproducts.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            unisexproducts = unisexproducts.filter(category__category_name__in=categories)
            categories = Category.objects.filter(category_name__in=categories)

        if request.GET:
            if 'q1' in request.GET:
                query = request.GET['q1']
                if not query:
                    messages.error(request, "No search criteria entered!")
                    return redirect(reverse('unisexproducts'))
                queries = Q(product_name__icontains=query) | Q(
                    description__icontains=query)
                unisexproducts = unisexproducts.filter(queries)
                 
                    
    existing_sorting = f'{sort}_{direction}'

    context = {
        'unisexproducts': unisexproducts,
        'search_term': query,
        'existing_categories': categories,
        'existing_sorting': existing_sorting,
        'image': image,

    }
    return render(request, 'product/unisex_product.html', context)

@login_required
def add_product(request):
    """
    add product to the page
    option only for superuser
    """
    if not request.user.is_superuser:
        messages.warning(request, 'Access denied,\
             only admin has access to this page')
        return redirect(reverse('all_products'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you!, product added succesfully!')
            return redirect(reverse('all_products'))
        else:
            messages.error(request,
                           ('Sorry! Something went wrong,\
                                Please recheck the form and try again.'))
    else:
        form = ProductForm()

    template = 'product/add_product.html'

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """edit/update product and its info from the page"""
    if not request.user.is_superuser:
        messages.warning(request, 'Access denied,\
            only admin has access to this')
        return redirect(reverse('all_products'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'product updated!')
            return redirect(reverse('all_products'))
        else:
            messages.error(request, 'Sorry,\
            request failed, please re-check the form and try again')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.product_name}')

    template = 'product/edit_product.html'
    context = {
        'form': form,
        'product': product,
        'product_id': product_id,
        'on_edit_page': True
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete product from the page """
    if not request.user.is_superuser:
        messages.warning(request, 'Access denied,\
             only admin has access to this')
        return redirect(reverse('all_products'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'product deleted!')
    return redirect(reverse('all_products'))