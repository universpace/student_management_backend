from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status




class StudentTest(APITestCase):
    def setUp(self):
        self.url = reverse('student')

    def test_post_user_data(self):
        data = {
            "words": ["death", "fear", "kill", "pray", "god", "hope", "pretty"]
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
