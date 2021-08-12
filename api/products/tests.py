from http import client

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status

from api.products.models import Product, Order
from api.products.serializers import ProductSerializer, OrderSerializer
from rest_framework.test import APIRequestFactory


class GetAllProductsTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        Product.objects.create(
            title='Ropa 1', description='Articulo de ropa # 1', price=100)
        Product.objects.create(
            title='Ropa 2', description='Articulo de ropa # 2', price=150)
        Product.objects.create(
            title='Ropa 3', description='Articulo de ropa # 3', price=200)
        Product.objects.create(
            title='Ropa 4', description='Articulo de ropa # 4', price=1000)

    def test_get_all_products(self):
        # get API response
        factory = APIRequestFactory()
        response = factory.get('/api/v1/products')
        # get data from db
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllOrdersTest(TestCase):

    def test_get_all_orders(self):
        # get API response
        factory = APIRequestFactory()
        response = factory.get('/api/v1/vieworders')
        # get data from db
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)