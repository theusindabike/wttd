from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):

    def test_form_has_fields(self):
        """ Form must have 4 fields """
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digits(self):
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form, 'cpf', 'digits_error')

    def test_cpf_has_11_digits(self):
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length_error')

    def test_name_must_be_capitalized(self):
        form = self.make_validated_form(name='MATHEUS Lopes')
        self.assertEqual('Matheus Lopes', form.cleaned_data['name'])

    def assertFormErrorCode(self, form, field, code):
        error_data = form.errors.as_data()
        e = error_data[field][0]
        self.assertEqual(code, e.code)

    def make_validated_form(self, **kwargs):
        valid = dict(
            name='Matheus Lopes',
            cpf='12345678901',
            email='email@matheus.com',
            phone='19999999999'
        )
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form
