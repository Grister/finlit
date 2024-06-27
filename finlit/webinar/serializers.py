from rest_framework import serializers

from webinar import models


class WebinarTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WebinarTag
        fields = "__all__"


class WebinarReadSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(slug_field='name', queryset=models.WebinarTag.objects.all(), many=True)
    speaker = serializers.StringRelatedField()

    class Meta:
        model = models.Webinar
        fields = "__all__"


class WebinarWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Webinar
        fields = "__all__"

