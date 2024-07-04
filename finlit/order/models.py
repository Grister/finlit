from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class Order(models.Model):
    CREATED = 1
    PAID = 2
    CANCELED = 0
    STATUSES = (
        (CREATED, 'Created'),
        (PAID, 'Paid'),
        (CANCELED, 'Canceled')
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name} - {self.content_object.name}'
