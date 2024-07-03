from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = "password",


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = "__all__"

    def validate(self, data):
        if data["email"]:
            if UserModel.objects.filter(email=data["email"]).exists():
                raise serializers.ValidationError("Email is already registered.")
            validate_email(data['email'])
        if data['password']:
            validate_password(data['password'])
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = UserModel
        exclude = "password",

    def validate_email(self, value):
        instance = self.instance
        if instance and instance.email != value and UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
