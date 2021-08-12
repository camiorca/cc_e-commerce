from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.IntegerField()


class Payment(models.Model):
    type = models.CharField(max_length=50)
    amount = models.IntegerField()
    status = models.BooleanField()


class OrderItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Shipment(models.Model):
    status = models.CharField(max_length=50)
    created_on = models.DateField()
    delivered_on = models.DateField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_value = models.IntegerField()
    address = models.CharField(max_length=50)
    created_on = models.DateField()
    items = models.ManyToManyField(OrderItem)
    payments = models.ManyToManyField(Payment)
    shipments = models.ManyToManyField(Shipment)


class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()
    sec_code = models.IntegerField()
