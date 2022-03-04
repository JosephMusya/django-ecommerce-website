from random import choice
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_resized import ResizedImageField

MAX_H,MAX_W = 300,300
# Create your models here.

class Category(models.Model):
    names = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.names

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    img = models.ImageField(upload_to = 'products',null=True) 
    name = models.CharField(max_length=100,blank=True)
    description = models.TextField(max_length=200, blank=True)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True,blank=True)
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)


    class Meta:
        ordering = ['-updated_at']
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=True)
    created_at = models.DateField(auto_now_add=True)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=150, blank=False)
    l_name = models.CharField(max_length=150, blank=False)
    phone = models.CharField(max_length=150, blank=False)
    town = models.CharField(max_length=150, blank=False)
    email = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    track_no = models.CharField(max_length=200, blank=False)
    #status = models.CharField(max_length=50)
    receipt = models.FileField(upload_to = 'static', null=True)
    order_status = (
        ('Pending','Pending'),
        ('Dispatched','Dispatched'),
        ('Delivered','Delivered'),
    )
    status = models.CharField(max_length=50,
                              choices=order_status,
                              default='Pending')
    
    updated_at = models.DateTimeField(auto_now=True,null=True)

    class Meta:
        ordering = ['-updated_at']
    def __str__(self):
        return '{}-{}'.format(self.id, self.track_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    
    def __str__(self):
        return '{} {} '. format(self.order.id, self.order.track_no)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=150, blank=False)
    l_name = models.CharField(max_length=150, blank=False)
    phone = models.CharField(max_length=150, blank=False)
    town = models.CharField(max_length=150, blank=False)
    email = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username