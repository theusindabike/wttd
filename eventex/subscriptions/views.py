from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def empty_form(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html',
                      {'form': form})

    s = Subscription.objects.create(**form.cleaned_data)

    _send_mail('subscriptions/subscription_email.txt',
               {'subscription': s},
               'Confirmação de inscrição',
               settings.DEFAULT_FROM_EMAIL,
               s.email)
    request.session['subscription_id'] = s.pk
    return HttpResponseRedirect(r('subscriptions:detail'))


def _send_mail(template_name, context, subject, from_, to):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])


def detail(request):
    try:
        pk = request.session['subscription_id']
        s = Subscription.objects.get(pk=pk)
        del request.session['subscription_id']
    except (Subscription.DoesNotExist, KeyError):
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html', {'subscription': s})
