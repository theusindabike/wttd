from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Matheus Lopes',
            slug='matheus-lopes',
            photo='https://avatars1.githubusercontent.com/u/3681926?s=460&v=4'
        )

    def test_email(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.EMAIL, value='matheus@email.com')
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(speaker=self.speaker, kind=Contact.PHONE, value='19999999999')
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker, kind=Contact.EMAIL, value='matheus@email.com')
        self.assertEqual('matheus@email.com', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Matheus Lopes',
            slug='matheus-lopes',
            photo='https://avatars1.githubusercontent.com/u/3681926?s=460&v=4',
        )

        s.contact_set.create(kind=Contact.EMAIL, value='matheus@email.com')
        s.contact_set.create(kind=Contact.PHONE, value='19999999999')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['matheus@email.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phone(self):
        qs = Contact.objects.phones()
        expected = ['19999999999']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)    