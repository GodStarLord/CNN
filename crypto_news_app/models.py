from django.db import models

# Create your models here.
class Coins(models.Model):
    coin_name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=30)