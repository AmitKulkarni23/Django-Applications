from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from django.views.generic import UpdateView, View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from .utils import Mailchimp
from .mixins import CsrfExemptMixin

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = "base/forms.html"
    success_url = "/settings/email" # Builtin-methods by default it would go to get_absolute_url
    success_message = "Your email preferences have been updated. Thank You"

    def get_context_data(self, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(**kwargs)
        context["title"] = "Update Email Preferences"
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/?next=/settings/email")
        return super(MarketingPreferenceUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


class MailchimpWebHookView(CsrfExemptMixin, View):
    # If you want a get method def get()
    # How about CSRF - CsrfExemptMixin
    def post(self, request, *args, **kwargs):
        data = request.POST  # Usually ina dictionary method
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get('data[email]')
            response_status, response = Mailchimp().check_subscription_status(email)
            sub_status = response["status"]
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "Subscribed":
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed = (False, False)

            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))

        return HttpResponse("Thank You", status=200)


# def mailchimp_webhook_view(request):
#     data = request.POST # Usually ina dictionary method
#     list_id = data.get('data[list_id]')
#     if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type = data.get("type")
#         email = data.get('data[email]')
#         response_status, response = Mailchimp().check_subscription_status(email)
#         sub_status = response["status"]
#         is_subbed = None
#         mailchimp_subbed = None
#         if sub_status == "Subscribed":
#             is_subbed, mailchimp_subbed = (True, True)
#         elif sub_status == "unsubscribed":
#             is_subbed, mailchimp_subbed = (False, False)
#
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists():
#                 qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))
#
#     return HttpResponse("Thank You", status=200)