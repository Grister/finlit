from rest_framework import serializers

from webinar import models


class WebinarTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WebinarTag
        fields = "__all__"


class WebinarReadSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.WebinarTag.objects.all(),
        many=True
    )
    speaker = serializers.StringRelatedField()
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = models.Webinar
        fields = "__all__"


class WebinarWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Webinar
        fields = "__all__"
