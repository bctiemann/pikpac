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

from accounts.models import Card
from api import serializers, filters

import logging
logger = logging.getLogger(__name__)


class CardViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CardSerializer

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def get_token(self, request):
        print(request.GET)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        token = stripe.Token.retrieve(request.GET['token'])

        return Response(token, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def add(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print(request.data)

        try:
            stripe_card = stripe.Customer.create_source(
                request.user.stripe_customer,
                source=request.data['token']['id'],
                # source='tok_chargeCustomerFail',
            )
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})

            print("Status is: %s" % e.http_status)
            print("Type is: %s" % err.get('type'))
            print("Code is: %s" % err.get('code'))
            # param is '' in this case
            print("Param is: %s" % err.get('param'))
            print("Message is: %s" % err.get('message'))

            return Response({'status': 'error', 'error': err})

        card = Card.objects.create(
            stripe_card=stripe_card.id,
            user=request.user,
            brand=stripe_card.brand,
            last_4=stripe_card.last4,
            exp_month=stripe_card.exp_month,
            exp_year=stripe_card.exp_year,
            fingerprint=stripe_card.fingerprint,
        )
        request.user.default_card = card
        request.user.save()
        serializer = self.get_serializer(data=model_to_dict(card))
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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


# class StripeCardView(APIView):
#
#     def post(self, request):
#         response = {}
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#
#         logger.info(request.data)


class StripeChargeView(APIView):

    def post(self, request):
        response = {}
        stripe.api_key = settings.STRIPE_SECRET_KEY

        print(request.data)
        logger.info(request.data)
        total_cents = int(request.data['total'] * 100)

        for cart_item in request.data['cart']:
            print(cart_item['order'])

        order_numbers = [c['order']['order_number'] for c in request.data['cart']]

        try:
            charge = stripe.Charge.create(
                amount=total_cents,
                currency="usd",
                # source=request.data['token'],  # obtained with Stripe.js
                source=request.user.default_card.stripe_card,
                customer=request.user.stripe_customer,
                description='Charge for order(s) {0}'.format(', '.join(order_numbers))
            )
            print(charge)
            print(charge['outcome'])
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})

            print("Status is: %s" % e.http_status)
            print("Type is: %s" % err.get('type'))
            print("Code is: %s" % err.get('code'))
            # param is '' in this case
            print("Param is: %s" % err.get('param'))
            print("Message is: %s" % err.get('message'))

            return Response({'status': 'error', 'error': err})

        response['status'] = 'ok'
        response['total_charged'] = total_cents / 100
        response['cart_details'] = request.data['cart']

        return Response(response)


