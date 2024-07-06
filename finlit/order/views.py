from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from order.models import Order
from order import serializer


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = serializer.OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = serializer.OrderStatusSerializer
        return super().partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = serializer.OrderCreateSerializer
        user = self.request.user.id
        request.data["user"] = user
        return super().create(request, *args, **kwargs)
