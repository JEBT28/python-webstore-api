# Generated by Django 4.1.3 on 2022-11-27 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
        ('carts', '0003_alter_cart_id_product_alter_cart_id_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='productos.producto'),
        ),
    ]
