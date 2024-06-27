from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet
from webinar import models, serializers


class WebinarViewSet(ModelViewSet):
    queryset = models.Webinar.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            self.serializer_class = serializers.WebinarReadSerializer
        else:
            self.serializer_class = serializers.WebinarWriteSerializer
        return super().get_serializer_class()


class WebinarTagViewSet(ModelViewSet):
    queryset = models.WebinarTag.objects.all()
    serializer_class = serializers.WebinarTagSerializer
    lookup_field = "id"
