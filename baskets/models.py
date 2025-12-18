from django.db import models

# Create your models here.
class Basket(models.Model): 
    PENDING = 'Pending' #these are the options transferred to the resource instance
    COMPLETED = 'Completed'
    OPEN =  'Open'
    
    STATUS_CHOICES = {  # these are the options displayed by the django admin website
        PENDING: 'Pending_KD', 
        COMPLETED: 'Completed_KD',
        OPEN: 'Open_KD'
    }
    
    name = models.CharField(max_length = 255)
    store = models.CharField (max_length = 255,blank=True, null=True )
    created_at = models.DateTimeField (auto_now_add=True)
    
    status = models.CharField(
        max_length = 100,
        choices = STATUS_CHOICES,
        default = PENDING
    )

    owner = models.ForeignKey(
        to = 'users.User',
        on_delete = models.CASCADE, 
        related_name = 'baskets_owned'
    )
    
    shared_with = models.ManyToManyField(
        to = 'users.User',
        related_name = 'baskets_shared', 
        blank = True
    )
    
    def __str__(self):
        my_string = self.name 
        if self.store: 
            my_string = my_string + f" ({self.store})"
        return my_string