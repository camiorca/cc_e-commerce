import random
import asyncio
import httpx
from django.contrib.auth import login
from django.http import JsonResponse
from flask import jsonify
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.models import AuthToken
from .models import Product, CreditCard, Payment, Shipment, Order, OrderItem
from .serializers import UserSerializer, RegisterSerializer, ProductSerializer, CreditCardSerializer, \
    ShipmentSerializer, OrderSerializer
from knox.views import LoginView as KnoxLoginView
from .validators import InfoValidations
from .utils import UtilityFunctions


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProductViewSet(viewsets.ModelViewSet):
    """
        Allows functions within the Product model.
        get:
        Return a list of all the existing products.

        post:
        Create a new product instance.
    """
    queryset = Product.objects.filter()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class CreditCardViewSet(viewsets.ModelViewSet):
    serializer_class = CreditCardSerializer
    permission_classes = [permissions.IsAuthenticated]
    user = Token.objects.filter()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = CreditCard.objects.filter(user=self.request.user.id)

        return queryset


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    user = Token.objects.filter()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    user = Token.objects.filter()


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class PurchaseViewSet(generics.GenericAPIView):
    """
        get:
        Return a list of all existing purchases by user

        post:
        Create a new user instance.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #Verify products and payment options
        products = []
        total_price = 0
        product_list = request.data['products']
        if len(product_list) == 0:
            return JsonResponse(status=500, data={'msg': 'No products added'})
        else:
            items = UtilityFunctions.calculate_total_price(None, product_list)
            if len(items['items']) == 0 or 'items' not in items.keys():
                return JsonResponse(status=500, data={'msg': 'No products were added or an item was not found'})
            else:
                products = items['items']
                total_price += items['total_cost']

        payment_option = request.data['payment_option']
        payments = UtilityFunctions.apply_payment(None, payment_option, request.data['payment_methods'], request.user.id)
        if len(payments) == 0:
            return JsonResponse(status=500, data={'msg': 'A payment method failed, please check again'})

        #Create Order
        order = UtilityFunctions.generate_order(None, request.user.id, total_price, request.data['address'])
        for order_item in products:
            p_id = order_item['product_id']
            quantity = order_item['quantity']
            temp = OrderItem.objects.create(
                product_id=Product.objects.get(id=p_id),
                quantity=quantity
            )
            temp.save()
            print(temp)
            order.items.add(temp)

        for pay in payments:
            temp_pay = Payment.objects.create(
                type=pay['type'],
                amount=pay['amount'],
                status=True
            )
            temp_pay.save()
            order.payments.add(temp_pay)

        order.save()

        return JsonResponse(status=200, data={'msg': 'Order created'})