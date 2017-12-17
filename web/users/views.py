from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.models import User
from users.utils import TwitterClient, WatsonClient

from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if not password:
            return Response(data="Password is required", status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data

        user = User.objects.create(**data)
        user.set_password(password)
        user.save()

        return Response(self.get_serializer(user).data)

    def update(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)

        serializer = self.get_serializer(user, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.save()

        return Response(self.get_serializer(user).data)

    @detail_route(methods=['POST'], url_path='update-statistics')
    def update_statistics(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)

        twitter_client = TwitterClient()
        twitter_data = twitter_client.send('statuses/user_timeline.json?screen_name={}&count=200'.format(user.twitter_handle))

        text = " ".join([content['text'] for content in twitter_data])

        watson_client = WatsonClient()
        watson_data = watson_client.send(
            'profile?version=2017-10-13',
            data={
                'content': text
            },
            method='post'
        )

        user.statistics = watson_data
        user.save()
        return Response(self.get_serializer(user).data)
