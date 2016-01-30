from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class TestRequestsList(TestCase):

    def setUp(self):
        # remember client
        self.client = Client()

    def test_view(self):
        """ test view with hard-coded data """
        response = self.client.get(reverse("requests_list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("http://example.com/blabla", response.content)
        self.assertEqual(len(response.context["objects"]), 2)
