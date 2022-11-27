from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto
from django.db.models.signals import pre_save
import uuid
# Create your models here.
# class Cart(models.Model):
#     cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
#     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) #relacion con usuario
#     products = models.ManyToManyField(Producto) #relacion con productos
#     subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2) #suma de precio de todos los productos
#     total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2) #subtotal mas iva
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.cart_id

# def set_cart_id(sender, instance, *args, **kwargs):
#     if not instance.cart_id: #si no posee identificador unico, se asigna un nuevo string
#         instance.cart_id = str(uuid.uuid4())

# pre_save.connect(set_cart_id, sender=Cart)


class Cart(models.Model):
    id_product = models.ForeignKey(Producto, on_delete=models.DO_NOTHING,related_name='producto')
    # id_product =models.IntegerField()
    quantity = models.IntegerField()
    cost =  models.FloatField()
    id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # id_user =models.IntegerField()

    def __str__(self):
        return str(self.id_product)

