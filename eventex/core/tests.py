from django.test import TestCase


class HomeTest(TestCase):
    def setUp(self):
        self.r = self.client.get("/")

    def test_get(self):
        """"GET / Must return status code 200 """
        self.assertEqual(200, self.r.status_code)


    def test_template(self):
        """"Must use index.html"""
        self.assertTemplateUsed(self.r, "index.html")
