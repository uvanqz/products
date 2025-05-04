from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_LIST = [
        ("processing", "В обработке"),
        ("accepted", "Принят"),
        ("delivered", "Доставлен"),
        ("canceled", "Отменён"),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_LIST, default="processing")

    def __str__(self):
        return self.status


# class Review(models.Model):
#     RAING_LIST = [
#         ("1", "1"),
#         ("2", "2"),
#         ("3", "3"),
#         ("4", "4"),
#         ("5", "5"),
#     ]
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     rating = models.CharField(max_length=1, choices=RAING_LIST)
#     comment = models.TextField(blank=True, null=True)
#     created_at = models.DateField(auto_now_add=True)
