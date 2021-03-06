from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from apps.requests.models import RequestEntry
import json
from django.conf import settings


class TestRequestsMiddlewareView(TestCase):

    def setUp(self):
        # remember client
        self.client = Client()

        self.url1 = reverse("requests_list")
        self.url2 = reverse("contacts_list")

    def test_middleware(self):
        """ test request middleware """
        self.client.get(self.url2)
        response = self.client.get(self.url1)
        # check if the proper template was used
        self.assertTemplateUsed(response, 'requests.html')
        self.assertIn(self.url1, response.content)
        # 2 requests are already done
        self.assertEqual(len(response.context["objects"]), 2)
        # default priority should be equal 1
        self.assertIn('Priority', response.content)
        self.assertEqual(response.context['objects'][0].priority, 1)
        # request to static url should have priority 0
        self.client.get(settings.STATIC_URL)
        self.failUnlessEqual(RequestEntry.objects.last().priority, 0)
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
        # last object should have id == 2
        self.assertTrue(response_data[-1]["id"] == 2)

    def test_ordering(self):
        """ test ordering: should have 2 modes. """
        RequestEntry.objects.create(method='GET',
                                    absolute_path=reverse('login'),
                                    is_ajax=False, priority=0)
        response = self.client.get(self.url)
        response_data = json.loads(response.content.decode())
        # should be ordered descending by priority if no params passed
        self.assertEqual(response_data[0]["priority"], 1)
        response = self.client.get(self.url, {'order': 0})
        response_data = json.loads(response.content.decode())
        # should be ordered ascending now
        self.assertEqual(response_data[0]["priority"], 0)
        self.assertEqual(response_data[1]["priority"], 1)
        self.assertEqual(response_data[2]["priority"], 1)
