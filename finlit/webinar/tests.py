from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from django.contrib.auth import get_user_model
from .models import Webinar, WebinarTag

UserModel = get_user_model()


# Models
class WebinarTagModelTest(TestCase):
    def test_create_webinar_tag(self):
        tag = WebinarTag.objects.create(name='Django')
        self.assertEqual(tag.name, 'Django')
        self.assertIsNotNone(tag.created_at)

    def test_webinar_tag_name_unique(self):
        WebinarTag.objects.create(name='Python')
        with self.assertRaises(Exception):
            WebinarTag.objects.create(name='Python')


class WebinarModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='test@example.com', password='testpassword')
        self.tag1 = WebinarTag.objects.create(name='Development')
        self.tag2 = WebinarTag.objects.create(name='Programming')

    def test_create_webinar(self):
        webinar = Webinar.objects.create(
            name='Learn Django',
            video_link='http://example.com/django',
            price=49.99,
            speaker=self.user
        )
        webinar.tags.add(self.tag1, self.tag2)
        self.assertEqual(webinar.name, 'Learn Django')
        self.assertEqual(webinar.video_link, 'http://example.com/django')
        self.assertEqual(webinar.price, 49.99)
        self.assertEqual(webinar.speaker, self.user)
        self.assertIn(self.tag1, webinar.tags.all())
        self.assertIn(self.tag2, webinar.tags.all())
        self.assertEqual(webinar.status, Webinar.PLANNED)


# API Views
class WebinarTagViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag1 = WebinarTag.objects.create(name='Django')
        self.tag2 = WebinarTag.objects.create(name='Python')
        self.tag_url = reverse('webinar:webinartag-list')

    def test_get_all_tags(self):
        response = self.client.get(self.tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_tag(self):
        data = {'name': 'REST'}
        response = self.client.post(self.tag_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WebinarTag.objects.count(), 3)
        self.assertEqual(WebinarTag.objects.get(name='REST').name, 'REST')

    def test_update_tag(self):
        url = reverse('webinar:webinartag-detail', args=[self.tag1.id])
        data = {'name': 'Django REST'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag1.refresh_from_db()
        self.assertEqual(self.tag1.name, 'Django REST')

    def test_delete_tag(self):
        url = reverse('webinar:webinartag-detail', args=[self.tag2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WebinarTag.objects.count(), 1)


class WebinarViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(email='test@example.com', password='testpassword')
        self.tag1 = WebinarTag.objects.create(name='Django')
        self.webinar_url = reverse('webinar:webinar-list')
        self.webinar = Webinar.objects.create(
            name='Learn Django',
            video_link='http://example.com/django',
            price=49.99,
            speaker=self.user
        )
        self.webinar.tags.add(self.tag1)

    def test_get_all_webinars(self):
        response = self.client.get(self.webinar_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_webinar(self):
        data = {
            'name': 'Learn REST',
            'video_link': 'http://example.com/rest',
            'price': 59.99,
            'speaker': self.user.id,
            'tags': [self.tag1.id]
        }
        response = self.client.post(self.webinar_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Webinar.objects.count(), 2)
        self.assertEqual(Webinar.objects.get(name='Learn REST').name, 'Learn REST')

    def test_update_webinar(self):
        url = reverse('webinar:webinar-detail', args=[self.webinar.id])
        data = {
            'name': 'Learn Django Advanced',
            'video_link': 'http://example.com/django-advanced',
            'price': 69.99,
            'speaker': self.user.id,
            'tags': [self.tag1.id]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.webinar.refresh_from_db()
        self.assertEqual(self.webinar.name, 'Learn Django Advanced')

    def test_delete_webinar(self):
        url = reverse('webinar:webinar-detail', args=[self.webinar.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Webinar.objects.count(), 0)
