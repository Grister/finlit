from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    content_type = serializers.StringRelatedField()
    object_id = serializers.CharField(source='content_object.name', read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate_content_type(self, value):
        allowed_models = ['course', 'webinar', 'consultation']
        if value.model not in allowed_models:
            raise serializers.ValidationError(f'Model "{value.model}" is not allowed.')
        return value


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
