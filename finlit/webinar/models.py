from django.db import models


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
    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['price'], name='price_idx'),
        ]

    def __str__(self):
        return f'{self.name}|{self.status}'

    @property
    def tags(self):
        return self.webinartag_set.all()


class WebinarTag(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    webinar = models.ForeignKey(to=Webinar, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = "name", "webinar"

    def __str__(self):
        return f'{self.name}|{self.webinar.name}'
