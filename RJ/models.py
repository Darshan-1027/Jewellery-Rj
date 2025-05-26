from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.

Status = [("Available","Available"),("Unavailable","Unavailable")]

class CategorysModel(models.Model):
    Name = models.CharField(max_length=20,unique=True)
    Image = models.ImageField(upload_to="Category_photos")

    def cat_photos(self):
        if self.Image:
            return mark_safe(f'<img src="{self.Image.url}" width="100px" />')
        return "No Image"
    
    def __str__(self):
        return self.Name
    
class ProductModel(models.Model):
    Category = models.ForeignKey(CategorysModel,on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Price = models.FloatField()
    First_Image = models.ImageField(upload_to="Products/") 
    Second_Image = models.ImageField(upload_to="Products/")
    Material = models.CharField(max_length=30)
    Length= models.CharField(max_length=10)
    Waight = models.CharField(max_length=10)
    Type_Of_work = models.CharField(max_length=20)
    Availability = models.CharField(max_length=20,choices=Status)
    Timestamp = models.DateTimeField(auto_now=True)

    def First(self):
        return mark_safe(f"<img src='{self.First_Image.url}' width='100px' />")
    
    def Second(self):
        return mark_safe(f"<img src='{self.Second_Image.url}' width='100px' />")
    
    def __str__(self):
        return self.Name
    

class RegisterDataModel(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    address = models.TextField()

class Order(models.Model):
    customer_name = models.CharField(max_length=100,default="Unknown")
    phone_number = models.CharField(max_length=15,default="Unknown")
    state = models.CharField(max_length=50,default="Gujarat")
    city = models.CharField(max_length=50, default='Ahmedabad')
    pincode = models.CharField(max_length=10,default="Unknown")
    address = models.TextField(null=True)
    # other fields...

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.Name} x {self.quantity} for Order #{self.order.id}"

from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField('RegisterDataModel', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.first_name} {self.user.last_name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.Price * self.quantity

    def __str__(self):
        return f"{self.product.Name} x {self.quantity}"


    
