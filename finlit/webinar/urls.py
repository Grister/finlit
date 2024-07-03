from django.urls import path, include
from rest_framework.routers import SimpleRouter

from webinar import views

app_name = 'webinar'

router = SimpleRouter()

router.register('webinar', views.WebinarViewSet, 'webinar')
router.register('webinar-tag', views.WebinarTagViewSet, 'webinartag')

urlpatterns = [
    path('', include(router.urls)),
]
