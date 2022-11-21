from django.db import models

# Create your models here.
class Producto(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()
    img_url = models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.name
    