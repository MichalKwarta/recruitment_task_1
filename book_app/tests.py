from django.db.utils import IntegrityError as DjangoIntegrityError
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from book_app.models import Book

# Create your tests here.
class BookTest(TestCase):
    def testEmptyInstanceCreation(self):
        instance = Book.objects.create()
        self.assertTrue(isinstance(instance, Book))

    def testNegativePageCount(self):

        with self.assertRaises(DjangoIntegrityError) as context:
            Book.objects.create(title="Test", author="Test", page_count=-1)
        self.assertTrue("CHECK constraint failed" in str(context.exception))

    def testWrongUrl(self):

        Book.objects.create(title="Test", author="Test", cover_url="wrong_url")


class APITest(TestCase):
    def testEmptyApiResponse(self):
        c = Client()
        response = c.get(reverse("API"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")

    def testAPI(self):
        c = Client()
        response = c.get(reverse("API"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")
        Book.objects.create(title="TestTitle", author="Test", cover_url="wrong_url")
        response = c.get(reverse("API")).json()
        self.assertEqual(response[0]["fields"]["title"], "TestTitle")
