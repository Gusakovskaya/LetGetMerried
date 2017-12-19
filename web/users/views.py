import requests

from django.core.files.base import ContentFile
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from users.serializers import UserSerializer, LoginSerializer
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

        data = serializer.data

        twitter_client = TwitterClient()
        twitter_data = twitter_client.send('users/show.json?screen_name={}'.format(data['twitter_handle']))

        image_url = twitter_data['profile_image_url'].replace('_normal', '')
        image_content = requests.get(image_url)

        user = User.objects.create(**data)
        user.set_password(password)
        user.image.save('user_picture.jpg', ContentFile(image_content.content), save=False)
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

    @list_route(methods=['POST'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        user = get_object_or_404(User, username=data['username'])
        if user.check_password(data['password']):
            request.session['user_id'] = user.id
            return Response("You're logged in.")

    @list_route(methods=['GET'], url_path='is-auth')
    def is_auth(self, request):
        if 'user_id' not in request.session:
            return Response("Not authorized", status=status.HTTP_400_BAD_REQUEST)
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        return Response(self.get_serializer(user).data)