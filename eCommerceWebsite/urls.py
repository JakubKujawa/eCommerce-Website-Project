"""eCommerceWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from apps.cart.views import cart_detail, success
from apps.cart.webhook import webhook
from apps.core.views import frontpage, contact, about
from apps.coupon.api import api_can_use
from apps.store.api import api_add_to_cart, api_remove_from_cart, api_checkout, create_checkout_session
from apps.store.views import product_detail, category_detail, search
from apps.userprofile.views import signup, myaccount
from .sitemaps import StaticViewSitemap, CategorySitemap, ProductSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'product': ProductSitemap,
    'category': CategorySitemap
}

urlpatterns = [
                  path('admin/', admin.site.urls),

                  # Frontpage

                  path('search/', search, name='search'),
                  path('cart/', cart_detail, name='cart'),
                  path('hooks/', webhook, name='webhook'),
                  path('cart/success/', success, name='success'),
                  path('', frontpage, name='frontpage'),
                  path('contact/', contact, name='contact'),
                  path('about/', about, name='about'),

                  # Auth
                  path('myaccount/', myaccount, name='myaccount'),
                  path('signup/', signup, name='signup'),
                  path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
                  path('logout/', views.LogoutView.as_view(), name='logout'),

                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

                  # API

                  path('api/can_use/', api_can_use, name='api_can_use'),
                  path('api/create_checkout_session/', create_checkout_session, name='create_checkout_session'),
                  path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
                  path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
                  path('api/checkout/', api_checkout, name='api_checkout'),

                  # Store

                  path('<slug:category_slug>/<slug:slug>/', product_detail, name='product_detail'),
                  path('<slug:slug>/', category_detail, name='category_detail'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
