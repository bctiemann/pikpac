import stripe
from requests import HTTPError

from django.conf import settings
from django.forms.models import model_to_dict
from django.contrib.auth import (
    login, logout, authenticate, get_user_model, password_validation,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from accounts.models import User, Address, Card
from products.models import ProductCategory, Product, ProductPrice, Pattern, Paper
from orders.models import Project, Order, Design, TaxRate, ShippingOption
from faq.models import FaqCategory, FaqHeading, FaqItem
from api import serializers, filters

import logging
logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Order.objects.all()
        if not self.request.GET.get('include_cancelled'):
            queryset = queryset.exclude(is_cancelled=True)
        return queryset
