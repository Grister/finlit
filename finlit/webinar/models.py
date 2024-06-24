from django.db import models
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class WebinarTag(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Webinar(models.Model):
    PLANNED = 1
    ONLINE = 2
    FINISHED = 3
    CANCELED = 0
    STATUSES = (
        (PLANNED, 'Planned'),
        (ONLINE, 'Online'),
        (FINISHED, 'Finished'),
        (CANCELED, 'Canceled')
    )

    name = models.CharField(max_length=256)
    video_link = models.URLField()
    price = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    old_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.SmallIntegerField(default=PLANNED, choices=STATUSES)
    description = models.TextField(null=True, blank=True)
    speaker = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='webinars')
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(to=WebinarTag)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['price'], name='price_idx'),
        ]

    def __str__(self):
        return f'{self.name}|{self.status}'
