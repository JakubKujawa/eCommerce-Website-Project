import random
from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Category, ProductReview
from ..cart.cart import Cart


def search(request):
    query = request.GET.get('query')
    instock = request.GET.get('instock')
    price_from = request.GET.get('price_from', 0)
    price_to = request.GET.get('price_to', 100000)
    sorting = request.GET.get('sorting', '-date_added')
    category = request.GET.get('category', 'all')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(
            price__gte=price_from).filter(price__lte=price_to)

    if category != 'all':
        products = products.filter(category__title__exact=category)

    if instock:
        products = products.filter(num_available__gte=1)

    paginator = Paginator(products.order_by(sorting), 1)
    page_number = request.GET.get('page')
    products_list = paginator.get_page(page_number)

    context = {
        'query': query,
        'products': products_list,
        'instock': instock,
        'price_from': price_from,
        'price_to': price_to,
        'sorting': sorting,
        'category': category
    }

    return render(request, 'search.html', context)


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    product.num_visits = product.num_visits + 1
    product.last_visit = datetime.now()
    product.save()

    # Add review

    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')

        ProductReview.objects.create(product=product, user=request.user, stars=stars, content=content)

        return redirect('product_detail', category_slug=category_slug, slug=slug)

    #

    related_products = list(product.category.products.filter(parent=None).exclude(id=product.id))

    if len(related_products) >= 3:
        related_products = random.sample(related_products, 3)

    if product.parent:
        return redirect('product_detail', category_slug=category_slug, slug=product.parent.slug)

    images_string = f"{{'thumbnail': '{product.get_thumbnail()}', 'image': '{product.image.url}'}}, "

    for image in product.images.all():
        images_string = images_string + (f"{{'thumbnail': '{image.thumbnail.url}', "
                                         f"'image': '{image.image.url}'}}, ")

    cart = Cart(request)

    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False

    context = {
        'product': product,
        'images_string': images_string,
        'related_products': related_products
    }

    return render(request, 'product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(parent=None)

    paginator = Paginator(products, 1)
    page_number = request.GET.get('page')
    products_list = paginator.get_page(page_number)

    context = {
        'category': category,
        'products': products_list
    }

    return render(request, 'category_detail.html', context)
