from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import Webinar, WebinarTag

UserModel = get_user_model()


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
