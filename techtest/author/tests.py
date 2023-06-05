import json

from django.test import TestCase
from django.urls import reverse

from techtest.author.models import Author

# Create your tests here.

class AuthorTestCase(TestCase):
    def setUp(self):
        self.url = reverse('author')
        self.author = Author.objects.create(first_name="John", last_name="Doe")
        self.author_2 = Author.objects.create(first_name="Jane", last_name="Doe")
        
    def test_serializes_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            [
                {
                    "id": self.author.id,
                    "first_name": "John",
                    "last_name": "Doe",
                },
                {
                    "id": self.author_2.id,
                    "first_name": "Jane",
                    "last_name": "Doe",
                },
            ],
        )
        
    def test_serializes_with_correct_data_shape_and_status_code_with_id(self):
        response = self.client.get(self.url + str(self.author.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            {
                "id": self.author.id,
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        
    def test_post(self):
        response = self.client.post(self.url, json.dumps({"first_name": "John", "last_name": "Doe"}), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertCountEqual(
            response.json(),
            {
                "id": 3,
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        
    def test_put(self):
        response = self.client.put(self.url + str(self.author.id) + '/', json.dumps({"first_name": "John", "last_name": "Dewy"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            {
                "id": self.author.id,
                "first_name": "John",
                "last_name": "Dewy",
            },
        )
        
    def test_delete(self):
        response = self.client.delete(self.url + str(self.author.id) + '/')
        self.assertEqual(response.status_code, 204)
        
        
