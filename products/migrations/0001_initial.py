# Generated by Django 4.0.7 on 2023-03-06 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('image_url', models.TextField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=20)),
                ('stock', models.IntegerField()),
                ('cart', models.ManyToManyField(related_name='cart_products', through='products.CartProducts', to='carts.cart')),
                ('order', models.ManyToManyField(related_name='ordered_products', to='orders.order')),
            ],
        ),
    ]
