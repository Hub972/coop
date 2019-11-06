from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class InfoUser(models.Model):
    """Contain user information"""
    number = models.IntegerField(null=True)
    street = models.CharField(max_length=200, default="contacter client par mail pour info")
    country = models.CharField(max_length=200)
    postalCode = models.IntegerField()
    telephone = models.IntegerField(null=True)
    information = models.CharField(max_length=600, null=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)


class Product(models.Model):
    """Contain product information"""
    CATCHOICE = [
        ('Fruit/Légume', 'Fruit/Légume'),
        ('Produit laitier', 'Produit laitier'),
        ('Charcuterie', 'Charcuterie'),
        ('Boisson', 'Boisson'),
        ('Divers', 'Divers')
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATCHOICE, default="Divers")
    disponibility = models.BooleanField(default=True)
    picture = models.ImageField(upload_to='pic/', null=True)
    information = models.CharField(max_length=600)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=00.00)
    idSeller = models.ForeignKey(User, on_delete=models.CASCADE)


class Bascket(models.Model):
    """Contain product ordered"""
    cmdNumber = models.IntegerField()
    quantity = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    idClient = models.ForeignKey(InfoUser, on_delete=models.CASCADE)
    idSeller = models.ForeignKey(User, on_delete=models.CASCADE, default=3)
    status = models.IntegerField(default=1)


class Delivery(models.Model):
    """Contain status product ordered"""
    deliveryNumber = models.IntegerField(primary_key=True, unique=True)
    status = models.IntegerField(default=1)
    deliveryAdrss = models.CharField(max_length=600)
    deliveryBool = models.BooleanField(default=True)
