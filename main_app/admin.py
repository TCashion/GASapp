from django.contrib import admin
from .models import Instrument, Accessory, InstrumentPhoto, AccessoryPhoto

# Register your models here.
admin.site.register(Instrument)
admin.site.register(Accessory)
admin.site.register(InstrumentPhoto)
admin.site.register(AccessoryPhoto)