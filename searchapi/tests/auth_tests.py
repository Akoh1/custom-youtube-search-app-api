from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from searchapi.models.user import User

# Create your tests here.
class AuthenticationTests(APITestCase):
	# def setUp(self):
 #        # Every test needs access to the request factory.
 #        self.factory = RequestFactory()
 #        self.user = User.objects.create_user(
 #            username='jacob', email='jacob@…', password='top_secret')
    def test_register_user(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register')
        data = {
        	'name': 'test',
        	'email': "test@gmail.com",
        	'password': "xxxx"
        }
        response = self.client.post(url, data, format='json')
        print(f"res: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@gmail.com')
