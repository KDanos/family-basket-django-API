from django.db import models

# Create your models here.
class Item (models.Model):
    ACTIVE = 'active' #these are the options transferred to the resource instance
    BOUGHT = 'bought'
    IGNORED =  'ignored'
    
    STATUS_CHOICES = {  # these are the options displayed by the django admin website
        ACTIVE : 'active', #these are the options transferred to the resource instance
        BOUGHT : 'bought',
        IGNORED :  'ignored'
    }

    name = models.CharField(max_length = 255)
    description = models.TextField
    
    status = models.CharField(
        max_length = 100,
        choices = STATUS_CHOICES,
        default = ACTIVE
    )    
    
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

