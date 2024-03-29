import stripe
from requests import HTTPError

from django.conf import settings
from django.forms.models import model_to_dict
from django.contrib.auth import (
    login, logout, authenticate, get_user_model, password_validation,
)
from django.utils.timezone import now
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action

from accounts.models import User, Address
from products.models import ProductCategory, Product, ProductPrice, Pattern, Paper
from orders.models import Project, Order, Design, DesignElement, TaxRate, ShippingOption
from faq.models import FaqCategory, FaqHeading, FaqItem
from api import serializers, filters

import logging
logger = logging.getLogger(__name__)


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

    permission_classes = ()
    serializer_class = serializers.ProjectSerializer
    filter_class = filters.ProjectTypeFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Project.objects.filter(
                Q(user=self.request.user) | Q(client_fingerprint=self.request.headers.get('Client-Fingerprint'))
            )
        return Project.objects.filter(client_fingerprint=self.request.headers.get('Client-Fingerprint'))
        # return Project.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        project = serializer.save()
        if request.user.is_authenticated:
            project.user = request.user
        project.client_fingerprint = request.headers.get('Client-Fingerprint')
        design = Design.objects.create(user=request.user, project=project)
        project.design = design
        project.save()
        order = Order.objects.create(project=project, user=request.user if request.user.is_authenticated else None)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    filter_class = filters.OrderStatusFilter

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        return queryset

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.status = Order.CANCELLED
        order.is_cancelled = True
        order.date_status_changed = now()
        order.save()

        return Response({'status': 'ok'})


class DesignViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DesignSerializer

    def get_queryset(self):
        return Design.objects.filter(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        print(request.data)
        pattern = None
        paper = None

        if request.data['pattern']:
            try:
                pattern = Pattern.objects.get(pk=request.data['pattern']['id'])
            except Pattern.DoesNotExist:
                return Response({'error': 'Invalid pattern'})

        if request.data['paper']:
            try:
                paper = Paper.objects.get(pk=request.data['paper']['id'])
            except Paper.DoesNotExist:
                return Response({'error': 'Invalid paper'})

        design = self.get_object()
        design.paper = paper
        design.pattern = pattern
        design.save()

        existing_element_ids = [d.id for d in design.design_elements.all()]
        new_element_ids = []
        for elem in request.data['design_elements']:
            print(elem)
            if elem['id']:
                design_elements = DesignElement.objects.filter(design=design, pk=elem['id'])
                design_elements.update(**elem)
                design_element = design_elements.first()
            else:
                design_element = DesignElement(**elem)
                design_element.design = design
                design_element.save()
            new_element_ids.append(design_element.id)
        elements_to_delete = list(set(existing_element_ids) - set(new_element_ids))
        DesignElement.objects.filter(pk__in=elements_to_delete).delete()

        return Response({})

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        design = serializer.save()
        design.user = request.user
        design.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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


class TaxRateView(APIView):

    def get(self, request, postal_code):
        try:
            tax_rate, created = TaxRate.objects.get_or_create(postal_code=postal_code)
        except HTTPError:
            return Response({'error': 'invalid postal code'}, status=status.HTTP_400_BAD_REQUEST)
        if (now() - tax_rate.date_updated).days > settings.TAXRATE_CACHE_DAYS:
            tax_rate.update()

        return Response({'total_rate': tax_rate.total_rate, 'date_updated': str(tax_rate.date_updated)})


class ShippingOptionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShippingOptionSerializer

    def get_queryset(self):
        return ShippingOption.objects.all()
