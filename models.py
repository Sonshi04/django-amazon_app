from itertools import product
from django.db import models

# Create your models here.
class Results(models.Model):
   keywords = models.CharField(max_length=100,default='amazon')
   min_price = models.IntegerField(default=0)
   max_price = models.IntegerField(default=0)
   product_num = models.IntegerField(default=0)
   image_data = models.CharField(max_length=10000,default='')
