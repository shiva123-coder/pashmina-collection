from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models.functions import Lower
from django.contrib import messages
from django.db.models import Q
from .models import(
    Category, Product, WomanProduct, ManProduct, KidsProduct, Variation)
from django.http import JsonResponse

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
def kids_products(request):
    kidsproducts = KidsProduct.objects.filter(is_available=True).order_by('product_name')
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
                kidsproducts = kidsproducts.annotate(sortkey=Lower("product_name"))

            if "direction" in request.GET:
                direction = request.GET["direction"]
                if direction == 'desc':
                    sortkey = f"-{'price'}"
                    if sortkey == "None":
                        kidsproducts = kidsproducts
                    else:
                        kidsproducts = kidsproducts.order_by(sortkey)
                else:
                    direction == 'asc'
                    sortkey = f"{'price'}"
                    if sortkey == "None":
                        kidsproducts = kidsproducts
                    else:
                        kidsproducts = kidsproducts.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            kidsproducts = kidsproducts.filter(category__category_name__in=categories)
            categories = Category.objects.filter(category_name__in=categories)

        if request.GET:
            if 'q1' in request.GET:
                query = request.GET['q1']
                if not query:
                    messages.error(request, "No search criteria entered!")
                    return redirect(reverse('kidsproducts'))
                queries = Q(product_name__icontains=query) | Q(
                    description__icontains=query)
                kidsproducts = kidsproducts.filter(queries)
                 
                    
    existing_sorting = f'{sort}_{direction}'

    context = {
        'kidsproducts': kidsproducts,
        'search_term': query,
        'existing_categories': categories,
        'existing_sorting': existing_sorting,
        'image': image,

    }
    return render(request, 'product/kids_product.html', context)