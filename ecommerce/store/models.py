from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return str(self.name).title()


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return str(self.name).title()


class Order(models.Model):
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    txn_id = models.AutoField(primary_key=True)

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for item in order_items:
            if not item.product.digital:
                shipping = True
                break
        return shipping

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        return sum([item.get_total for item in order_items])

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        return sum([item.quantity for item in order_items])

    def __str__(self):
        return str(self.txn_id)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=100, null=True)
    zipcode = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)
