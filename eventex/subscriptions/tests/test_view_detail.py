from django.test import TestCase
from django.shortcuts import resolve_url as r

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.s = Subscription.objects.create(
            name='Matheus Lopes',
            cpf='12345678901',
            email='email@matheus.com',
            phone='19999999999'
        )
        session = self.client.session
        session['subscription_id'] = self.s.pk
        session.save()

        self.resp = self.client.get(r('subscriptions:detail'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = (self.s.name, self.s.cpf, self.s.email, self.s.phone)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)

    def test_session_subscription_id_is_deleted_after(self):
        self.resp = self.client.get(r('subscriptions:detail'))
        self.assertEqual(404, self.resp.status_code)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get(r('subscriptions:detail'))
        self.assertEqual(404, resp.status_code)
