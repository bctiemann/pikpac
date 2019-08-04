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

from accounts.models import User
from products.models import ProductCategory, Product, ProductPrice, Pattern, Paper
from orders.models import Project, Order
from faq.models import FaqCategory, FaqHeading, FaqItem
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
        user.populate_instrument_skills()
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


class PasswordResetTokenCheckView(APIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.PasswordTokenCheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': 'OK'})


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
        return Project.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
