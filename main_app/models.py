from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

CONDITIONS = [
    ('U', 'Used'),
    ('P', 'Poor'),
    ('F', 'Fair'),
    ('G', 'Good'),
    ('V', 'Very Good'),
    ('E', 'Excellent'),
    ('M', 'Mint'),
    ('B', 'BrandNew'),
]

class Instrument(models.Model):
    name = models.CharField(max_length=150)
    instrument_type = models.CharField(max_length=150)
    manufacturer = models.CharField(max_length=150)
    serial = models.CharField(max_length=250)
    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators = [MinValueValidator(0.01, 'Price must be greater than $0.01')],
    )
    condition = models.CharField(
        max_length = 1,
        choices = CONDITIONS,
        default = CONDITIONS[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Name: {self.name}, Type: {self.instrument_type}"
    
    def get_absolute_url(self):
        return reverse('instruments_detail', kwargs={'instrument_id' : self.id})

