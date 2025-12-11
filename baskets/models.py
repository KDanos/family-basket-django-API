from django.db import models

# Create your models here.
class Basket(models.Model): 
    PENDING = 'pending'
    COMPLETED = 'completed'
    OPEN =  'open'
    
    STATUS_CHOICES = {
        PENDING: 'pending', 
        COMPLETED: 'completed',
        OPEN: 'open'
    }
    name = models.CharField(max_length = 255)
    store = models.CharField (max_length = 255,blank=True, null=True )
    created_at = models.DateTimeField (auto_now_add=True)
    
    status = models.CharField(
        max_length = 100,
        choices = STATUS_CHOICES,
        default = PENDING
    )

    def __str__(self):
        my_string = self.name 
        if self.store: 
            my_string = my_string + f" ({self.store})"
        return my_string