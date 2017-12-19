from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    twitter_handle = serializers.CharField(max_length=256, required=True)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'twitter_handle',
            'statistics',
            'latitude',
            'longitude',
            'image',
            'password'
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        if 'image' in data:
            data['image'] = instance.image.name
        return data
