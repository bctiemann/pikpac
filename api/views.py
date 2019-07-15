from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import (
    login, logout, authenticate, get_user_model, password_validation,
)

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from products.models import ProductCategory, Product, ProductPrice
from orders.models import Project
from . import serializers, filters


class LoginView(APIView):

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        response = {}
        print(request.data)
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

        return Response(response)


class LogoutView(APIView):

    def post(self, request, format=None):
        response = {}
        request.user.auth_token.delete()

        logout(request)

        return Response(response)


class MeView(APIView):

    def get(self, request):
        response = {
            'data': {
                'id': self.request.user.id,
                'username': self.request.user.email,
                'email': self.request.user.email,
                'first_name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
            }
        }
        return Response(response)


class ProductCategoryViewSet(viewsets.ModelViewSet):

    authentication_classes = ()
    permission_classes = ()

    serializer_class = serializers.ProductCategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return ProductCategory.objects.all()


class ProductViewSet(viewsets.ModelViewSet):

    authentication_classes = ()
    permission_classes = ()

    serializer_class = serializers.ProductSerializer
    filter_class = filters.ProductFilter

    def get_queryset(self):
        return Product.objects.all()

    @action(detail=True, methods=['post'])
    def price(self, request, pk=None):
        product = self.get_object()

        product_price = ProductPrice.objects.get(product=product, quantity=request.data['quantity'])

        return Response({'price': product_price.unit_price})


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
