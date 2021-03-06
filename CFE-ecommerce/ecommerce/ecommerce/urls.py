"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from .views import home_page, about_page, contact_page
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from carts.views import cart_home
from accounts.views import LoginView, guest_register_view, RegisterView
from django.contrib.auth.views import LogoutView
from adresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view
from billing.views import payment_method_view, payment_method_createview
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebHookView

urlpatterns = [
    path(r"", home_page, name="home"),
    path(r"about/", about_page, name="about"),
    path(r"contact/", contact_page, name="contact"),
    path(r"login/", LoginView.as_view(), name="login"),
    path(r"logout/", LogoutView.as_view(), name="logout"),
    path(r"register/", RegisterView.as_view(), name="register"),
    path("bootstrap", TemplateView.as_view(template_name="bootstrap/example.html")),
    path("products/", include("products.urls", namespace="products")),
    re_path(r"api/cart/$", cart_detail_api_view, name="api-cart"),
    path("cart/", include("carts.urls", namespace="carts")),
    path("billing/payment-method", payment_method_view, name="billing-payment-method"),
    path("billing/payment-method/create/", payment_method_createview, name='billing-payment-method-endpoint'),
    path("search/", include("search.urls", namespace="search")),
    path("register/guest/", guest_register_view, name="guest_register"),
    path("checkout/address/create", checkout_address_create_view, name="checkout_address_create"),
    path("checkout/address/reuse", checkout_address_reuse_view, name="checkout_address_reuse"),
    path("settings/email", MarketingPreferenceUpdateView.as_view(), name="marketing-pref"),
    path("webhooks/mailchimp/", MailchimpWebHookView.as_view(), name="webhooks-mailchimp"),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)