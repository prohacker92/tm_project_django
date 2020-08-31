from django.db import models

class Support_contacts (models.Model):
    position = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    numbers = models.CharField(max_length=254)

