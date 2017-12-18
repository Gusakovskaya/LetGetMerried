from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)

    twitter_handle = serializers.CharField(max_length=256, required=True)

    image = serializers.SerializerMethodField()

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
            'image'
        )

    def get_image(self, instance):
        return instance.image.name
