import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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


class Accessory(models.Model):
    name = models.CharField(max_length=150)
    accessory_type = models.CharField(max_length=150)
    manufacturer = models.CharField(max_length=150)
    year = models.IntegerField('Manufacture year (YYYY)', null=True, blank=True, validators=[
            MinValueValidator(1900, 'Year must be greater than 1900'),
            MaxValueValidator(max_year(), f"Year must be less than {max_year()}")
        ]
    )
    serial = models.CharField(max_length=250, blank=True, null=True)
    condition = models.CharField(max_length=1, choices=CONDITIONS, default=CONDITIONS[0][0])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owned = models.BooleanField('Do you own this accessory?', default=True)

    def __str__(self):
        return f"Name: {self.name}"

    def get_absolute_url(self):
        return reverse('accessories_detail', kwargs={'accessory_id': self.id})


class Instrument(models.Model):
    name = models.CharField(max_length=150)
    instrument_type = models.CharField(max_length=150)
    manufacturer = models.CharField(max_length=150)
    year = models.IntegerField('Manufacture year (YYYY)', null=True, blank=True, validators=[
        MinValueValidator(1900, 'Year must be greater than 1900'),
        MaxValueValidator(max_year(), f"Year must be less than {max_year()}")
        ]
    )
    serial = models.CharField(max_length=250, null=True, blank=True)
    condition = models.CharField(max_length=1, choices=CONDITIONS, default=CONDITIONS[0][0])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owned = models.BooleanField('Do you own this instrument?', default=True)
    accessories = models.ManyToManyField(Accessory)

    def __str__(self):
        return f"Name: {self.name}, Type: {self.instrument_type}"

    def get_absolute_url(self):
        return reverse('instruments_detail', kwargs={'instrument_id': self.id})


class InstrumentPhoto(models.Model):
    url = models.CharField(max_length=300)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for instrument_id: {self.instrument_id} @{self.url}"


class AccessoryPhoto(models.Model):
    url = models.CharField(max_length=300)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for accessory_id: {self.accessory_id} @{self.url}"
