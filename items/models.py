from django.db import models

# Create your models here.
class Item (models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField
    basket = models.ForeignKey(
        to = 'baskets.Basket',
        on_delete= models.CASCADE,
        related_name = 'basket_items'
    )
    creator = models.ForeignKey(
        to = 'users.User',
        on_delete=models.CASCADE,
        related_name =  'items_created'
    )

