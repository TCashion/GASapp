import datetime
from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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

def max_year(): 
    return datetime.date.today().year + 5

class Instrument(models.Model):
    name = models.CharField(max_length=150)
    instrument_type = models.CharField(max_length=150)
    manufacturer = models.CharField(max_length=150)
    year = models.IntegerField('Manufacture year (YYYY)',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1900, 'Year must be greater than 1900'),
            MaxValueValidator(max_year(), f"Year must be less than {max_year()}")]
    )
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


# class Accessory(models.Model):
#     name = models.CharField(max_length=150)
#     manufacturer = models.CharField(max_length=150)
#     year = models.IntegerField('Manufactur year (YYYY)',
#         null=True,
#         blank=True,
#         min_value=1900,
#         max_value=max_year(), 
#     )
#     serial = models.CharField(max_length=250, blank=True, null=True)
#     price = models.DecimalField(
#         max_digits=12, 
#         decimal_places=2,
#         validators = [MinValueValidator(0.01, 'Price must be greater than $0.01')],
#     )
#     condition = models.CharField(
#         max_length = 1,
#         choices = CONDITIONS,
#         default = CONDITIONS[0][0]
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Name: {self.name}, Type: {self.accessory_type}"
    
#     def get_absolute_url(self):
#         return reverse('accessories_detail', kwargs={'accessory_id' : self.id})