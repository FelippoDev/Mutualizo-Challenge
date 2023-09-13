# from django.db import models
# from ecommerce.user.models import User

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     quantity = models.PositiveIntegerField(default=1)

    
# class ShoppingCart(models.Model):
#     user = models.ForeignKey(User)
#     products = models.ManyToManyField()
    
    
# class Order(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     payment_method = models
#     user = models.ForeignKey(User)