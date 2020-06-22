from django.contrib import admin
from .models import Instrument, Accessory

# Register your models here.
admin.site.register(Instrument)
admin.site.register(Accessory)