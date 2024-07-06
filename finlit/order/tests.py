from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token
from order.models import Order
from webinar.models import Webinar

User = get_user_model()


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com', password='admin1234')
        self.user = User.objects.create_user(
            email='user@example.com', password='user1234')
        self.client = APIClient()

        self.admin_token = Token.objects.create(user=self.admin_user)
        self.user_token = Token.objects.create(user=self.user)

        # Create a Course, Webinar and Consultation for testing
        self.course = Webinar.objects.create(name='Test Course', price=12.00, speaker_id=self.user.id)
        self.webinar = Webinar.objects.create(name='Test Webinar', price=5.00, speaker_id=self.user.id)
        self.consultation = Webinar.objects.create(name='Test Consultation', price=20.00, speaker_id=self.user.id)

        # ContentTypes for the models
        self.course_content_type = ContentType.objects.get_for_model(Webinar)

        self.order_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'content_type': self.course_content_type,
            'object_id': self.course.id,
            'status': Order.CREATED,
            'user': self.user
        }

    def test_create_order(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post(reverse('order:order-list'), self.order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_list_orders_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(reverse('order:order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_list_orders_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get(reverse('order:order-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_retrieve_order_as_admin(self):
        order = Order.objects.create(**self.order_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(reverse('order:order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_retrieve_order_as_non_admin(self):
        order = Order.objects.create(**self.order_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get(reverse('order:order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_partial_update_order_as_admin(self):
        order = Order.objects.create(**self.order_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.patch(reverse('order:order-detail', args=[order.id]), {'status': Order.PAID})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_partial_update_order_as_non_admin(self):
        order = Order.objects.create(**self.order_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.patch(reverse('order:order-detail', args=[order.id]), {'status': Order.PAID})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_delete_order_as_admin(self):
        order = Order.objects.create(**self.order_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.delete(reverse('order:order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()

    def test_delete_order_as_non_admin(self):
        order = Order.objects.create(**self.order_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.delete(reverse('order:order-detail', args=[order.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
