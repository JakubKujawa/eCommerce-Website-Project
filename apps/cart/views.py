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
            f"'quantity': '{item['quantity']}', 'total_price': '{item['total_price']}', 'thumbnail': " \
            f"'{product.get_thumbnail()}', 'url': '{url}', 'num_available': '{product.num_available}'}}, "

        productsstring = productsstring + b

    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        address = request.user.userprofile.address
        zipcode = request.user.userprofile.zipcode
        place = request.user.userprofile.place
        phone = request.user.userprofile.phone
    else:
        first_name = last_name = email = address = zipcode = place = phone = ''

    context = {
        'cart': cart,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'address': address,
        'zipcode': zipcode,
        'place': place,
        'phone': phone,
        'pub_key': settings.STRIPE_API_KEY_PUBLISHABLE,
        'productsstring': productsstring
    }

    return render(request, 'cart.html', context)


def success(request):
    cart = Cart(request)
    cart.clear()

    return render(request, 'success.html')
