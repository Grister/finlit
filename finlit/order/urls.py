from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import OrderViewSet


app_name = 'user'

router = SimpleRouter()
router.register('order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
