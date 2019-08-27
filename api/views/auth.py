from django.conf import settings
from django.forms.models import model_to_dict
from django.contrib.auth import (
    login, logout, authenticate, get_user_model, password_validation,
)
from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from accounts.models import User
from orders.models import Project
from api import serializers, filters

import logging
logger = logging.getLogger(__name__)


class LoginView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        response = {}
        if not ('email' in request.data and ('password' in request.data or 'confirm_hashkey' in request.data)):
            raise ValidationError('Invalid request.')

        if 'password' in request.data:
            user = authenticate(username=request.data['email'], password=request.data['password'])

            if not user:
                raise ValidationError('Invalid login credentials.')

            if not user.is_active:
                raise ValidationError('User account has been disabled.')

            if not user.is_confirmed:
                raise ValidationError('User account has not been confirmed.')
            print('Login via password')

        else:
            try:
                user = User.objects.get(email=request.data.get('email'),
                                        confirm_hashkey=request.data.get('confirm_hashkey'))
            except User.DoesNotExist:
                raise ValidationError('Invalid hash key for this account.')
            print('Login via hashkey')
            user.confirm_hashkey = None
            user.save()

        auth_token, is_created = Token.objects.get_or_create(user=user)
        response['email'] = user.email
        response['token'] = auth_token.key

        login(request, user)

        # Claim projects created by this user (id'd by fingerprint) while logged out
        for project in Project.objects.filter(user=None, client_fingerprint=request.headers.get('Client-Fingerprint')):
            project.user = user
            project.save()

        return Response(response)


class LogoutView(APIView):

    def post(self, request, format=None):
        response = {}
        request.user.auth_token.delete()

        logout(request)

        return Response(response)


class MeView(GenericAPIView):

    serializer_class = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response({ 'data': serializer.data })


class RegisterView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        print(request.data)
        response = {'success': True}

        if not ('email' in request.data and 'password' in request.data):
            raise ValidationError('Invalid request.')

        user, created = User.objects.get_or_create(email=request.data.get('email'))
        if not created:
            raise ValidationError('A user with this email already exists.')

        user.set_password(request.data.get('password'))
        user.send_confirm()
        return Response(response)


class RegisterConfirmView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        response = {'success': False}
        try:
            user = User.objects.get(email=request.data.get('email'),
                                    confirm_hashkey=request.data.get('confirm_hashkey'))
        except User.DoesNotExist:
            raise ValidationError('Invalid hash key for this account.')
        print(user)

        user.is_confirmed = True
        user.save()

        response['success'] = True
        return Response(response)


