from django.db import models
from django.contrib.auth.models import User

from productos.models import Producto

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    direction = models.CharField(max_length=100)
    total = models.FloatField()
    
class orderDetail(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True,related_name='orderDetails')
