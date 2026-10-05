from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Category(models.Model):
    name = models.CharField(max_length=50)  # Category name 
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the category was created

    class Meta:
        ordering = ['name'] # Order categories by name in ascending order

    def __str__(self):
        return self.name  # Return the category name when the object is printed


class Product(models.Model):
    Categories = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign key to Category model
    name = models.CharField(max_length=100)  # Product name
    description = models.TextField()  # Product description
    price = models.DecimalField(decimal_places=2 , max_digits=8)  # Product price 
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the product was created
    Product_image = models.ImageField(upload_to='product_images/')  # Image field for product image
    def __str__(self):
        return self.name