from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import SAFE_METHODS, IsAdminUser

from user import serializers
from user.permissions import IsOwnerOrReadOnly, IsOwnerOrIsAdmin

UserModel = get_user_model()


class UserListAPIView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.request.method != "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.UserSerializer
        return serializers.UserCreateSerializer


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = "id"
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.request.method in ["GET", "DELETE"]:
            self.permission_classes = [IsOwnerOrIsAdmin]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.UserSerializer
        return serializers.UserUpdateSerializer
