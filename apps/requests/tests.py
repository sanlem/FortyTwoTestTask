from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
import json


class TestRequestsMiddlewareView(TestCase):

    def setUp(self):
        # remember client
        self.client = Client()

        self.url1 = reverse("requests_list")
        self.url2 = reverse("contacts_list")

    def test_middleware(self):
        """ test request middleware """
        response = self.client.get(self.url2)

        response = self.client.get(self.url1)
        self.assertIn(self.url1, response.content)
        self.assertEqual(len(response.context["objects"]), 2)

        # we only have to show last 10 requests
        for i in range(11):
            response = self.client.get(self.url1)
        self.assertEqual(len(response.context["objects"]), 10)


class TestRequestsListEndpoint(TestCase):

    def setUp(self):
        # remember client
        self.client = APIClient()

        self.url = reverse('requests_api')

    def test_list(self):
        """ test requests api endpoint.
            should return no more than 10 objects. """
        response = self.client.get(self.url)
        response_data = json.loads(response.content.decode())
        self.assertTrue(len(response_data), 1)
        for i in range(10):
            response = self.client.get(self.url)
        response_data = json.loads(response.content.decode())
        self.assertEqual(len(response_data), 10)
