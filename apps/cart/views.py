from django.conf import settings
from django.shortcuts import render

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    productsstring = ''

    for item in cart:
        product = item['product']
        url = f"/{product.category.slug}/{product.slug}/"
        b = f"{{'id': '{product.id}', 'title': '{product.title}', 'price': '{product.price}', " \
            f"'quantity': '{item['quantity']}', 'total_price': '{item['total_price']}', " \
            f"'thumbnail': '{product.thumbnail.url}', 'url': '{url}', 'num_available': '{product.num_available}'}}, "
        productsstring = productsstring + b

    context = {
        'cart': cart,
        'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
        'productsstring': productsstring
    }

    return render(request, 'cart.html', context)


def success(request):
    cart = Cart(request)
    cart.clear()

    return render(request, 'success.html')
