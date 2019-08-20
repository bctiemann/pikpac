import stripe
from requests import HTTPError

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
from api import serializers, filters

import logging
logger = logging.getLogger(__name__)


class StripeCustomerView(APIView):

    def post(self, request):
        response = {}
        stripe.api_key = settings.STRIPE_SECRET_KEY

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
#         stripe.api_key = settings.STRIPE_SECRET_KEY
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
        stripe.api_key = settings.STRIPE_SECRET_KEY

        logger.info(request.data)


class StripeChargeView(APIView):

    def post(self, request):
        response = {}
        stripe.api_key = settings.STRIPE_SECRET_KEY

        logger.info(request.data)

        charge = stripe.Charge.create(
            amount=101,
            currency="usd",
            source=request.data['token'],  # obtained with Stripe.js
            description="Charge for jenny.rosen@example.com"
        )
        response['status'] = 'ok'
        return Response(response)


