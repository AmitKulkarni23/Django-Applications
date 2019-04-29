from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .models import BillingProfile, Card

import stripe
stripe.api_key = "sk_test_DjVHt74y3ojZJJKuXM85Q3Aq00JNC0FkIO"
STRIPE_PUB_KEY = 'pk_test_y0LrxcrefvyUkATasoRO1jbZ00nhh2JLMV'


def payment_method_view(request):

    # If user is authenticated
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     customer_id = billing_profile.customer_id

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if not billing_profile:
        return redirect("/cart")

    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"})

        token = request.POST.get("token")
        if token:
            new_card_object = Card.objects.add_new(billing_profile, token)
            print(new_card_object)
            return JsonResponse({"message": "Success! Your card was added."})

    return HttpResponse("error", status=401)