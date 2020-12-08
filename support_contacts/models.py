from django.db import models


class SupportСontacts (models.Model):
    position = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    numbers = models.CharField(max_length=254)

