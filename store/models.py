from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class InfoUser(models.Model):
    number = models.IntegerField(null=True)
    street = models.CharField(max_length=200),
    country = models.CharField(max_length=200)
    postalCode = models.IntegerField()
    telephone = models.IntegerField(null=True)
    information = models.CharField(max_length=600, null=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)


class Seller(models.Model):
    job = models.CharField(max_length=100)
    number = models.IntegerField(null=True)
    street = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    postalCode = models.IntegerField()
    telephone = models.IntegerField(null=True)
    information = models.CharField(max_length=600, null=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    disponibility = models.BooleanField(default=True)
    picture = models.CharField(max_length=600, null=True)
    information = models.CharField(max_length=600)
    idSeller = models.ForeignKey(Seller, on_delete=models.CASCADE)


class Bascket(models.Model):
    cmdNumber = models.IntegerField()
    quantity = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    idClient = models.ForeignKey(InfoUser, on_delete=models.CASCADE)


class Delivery(models.Model):
    deliveryNumber = models.IntegerField(primary_key=True, unique=True)
    status = models.IntegerField(default=1)
    deliveryAdrss = models.CharField(max_length=600)
    deliveryBool = models.BooleanField(default=True)