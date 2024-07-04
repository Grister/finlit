from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from user import views

app_name = 'user'

urlpatterns = [
    path("auth/", ObtainAuthToken.as_view(), name="auth"),
    path("user/", views.UserListAPIView.as_view(), name="user-list"),
    path("user/<int:id>/", views.UserDetailAPIView.as_view(), name="user-detail"),
]
