from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    def total_price(self):
        return self.quantity * self.product.price
    # This will return the total price of the product in the cart

    def __str__(self):
        return f"{self.quantity} * {self.product.name}"