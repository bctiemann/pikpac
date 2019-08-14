import stripe

from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import (
    login, logout, authenticate, get_user_model, password_validation,
)

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from accounts.models import User, Address, Card
from products.models import ProductCategory, Product, ProductPrice, Pattern, Paper
from orders.models import Project, Order
from faq.models import FaqCategory, FaqHeading, FaqItem
from . import serializers, filters

import logging
logger = logging.getLogger(__name__)


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

        try:
            product_price = ProductPrice.objects.get(product=product, quantity=request.data['quantity'])
        except ProductPrice.DoesNotExist:
            return Response({'price': 0})

        return Response({'price': product_price.unit_price})


class PatternViewSet(viewsets.ModelViewSet):

    authentication_classes = ()
    permission_classes = ()

    serializer_class = serializers.PatternSerializer
    # filter_class = filters.ProductFilter

    def get_queryset(self):
        return Pattern.objects.all()


class PaperViewSet(viewsets.ModelViewSet):

    authentication_classes = ()
    permission_classes = ()

    serializer_class = serializers.PaperSerializer
    # filter_class = filters.ProductFilter

    def get_queryset(self):
        return Paper.objects.all()


class FaqCategoryViewSet(viewsets.ModelViewSet):

    authentication_classes = ()
    permission_classes = ()

    serializer_class = serializers.FaqCategorySerializer

    def get_queryset(self):
        return FaqCategory.objects.all()


class FaqHeadingViewSet(viewsets.ModelViewSet):

    authentication_classes = ()
    permission_classes = ()
    filter_class = filters.FaqHeadingFilter

    serializer_class = serializers.FaqHeadingSerializer

    def get_queryset(self):
        return FaqHeading.objects.all()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        print('a')
        serializer.is_valid(raise_exception=True)
        print(serializer)
        project = serializer.save()
        project.user = request.user
        project.save()
        order = Order.objects.create(project=project, user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def create(self, request, address_type):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.save()
        address.user = request.user
        address.save()
        if address_type == 'billing':
            request.user.billing_address = address
        elif address_type == 'shipping':
            request.user.shipping_address = address
        request.user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'])
    def billing(self, request, *args, **kwargs):
        print('billing')
        return self.create(request, address_type='billing')

    @action(detail=False, methods=['post'])
    def shipping(self, request, *args, **kwargs):
        return self.create(request, address_type='shippin')


class StripeCustomerView(APIView):

    def post(self, request):
        response = {}
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

        customer = stripe.Customer.create(
            email=request.user.email,
            description="Customer for jenny.rosen@example.com"
        )
        response['status'] = 'ok'
        return Response(response)


# class StripeCustomerView(APIView):
#
#     def post(self, request):
#         response = {}
#         stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
#
#         customer = stripe.Customer.create(
#             email=request.user.email,
#             description="Customer for jenny.rosen@example.com"
#         )
#         response['status'] = 'ok'
#         return Response(response)


class StripeCardView(APIView):

    def post(self, request):
        response = {}
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

        logger.info(request.data)


class StripeChargeView(APIView):

    def post(self, request):
        response = {}
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

        logger.info(request.data)

        charge = stripe.Charge.create(
            amount=101,
            currency="usd",
            source=request.data['token'],  # obtained with Stripe.js
            description="Charge for jenny.rosen@example.com"
        )
        response['status'] = 'ok'
        return Response(response)
