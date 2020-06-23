from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Instrument, Accessory, InstrumentPhoto, AccessoryPhoto
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'gas-app'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def index(request):
    instruments = request.user.instrument_set.order_by('name')
    accessories = request.user.accessory_set.order_by('name')
    return render(request, 'index.html', {
        'instruments': instruments,
        'accessories': accessories,
    })

@login_required
def instruments_detail(request, instrument_id):
    instrument = Instrument.objects.get(id=instrument_id)
    return render(request, 'instruments/detail.html', {'instrument': instrument})

@login_required
def accessories_detail(request, accessory_id):
    accessory = Accessory.objects.get(id=accessory_id)
    return render(request, 'accessories/detail.html', {'accessory': accessory})

class InstrumentCreate(LoginRequiredMixin, CreateView):
    model = Instrument
    fields = ['name', 'instrument_type', 'year', 'manufacturer', 'serial', 'price', 'condition', 'owned']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class InstrumentUpdate(LoginRequiredMixin, UpdateView):
    model = Instrument
    fields = ['name', 'instrument_type', 'year', 'manufacturer', 'serial', 'price', 'condition', 'owned']
    
class InstrumentDelete(LoginRequiredMixin, DeleteView):
    model = Instrument
    success_url = '/collections/'

class AccessoryCreate(LoginRequiredMixin, CreateView):
    model = Accessory
    fields = ['name', 'accessory_type', 'year', 'manufacturer', 'serial', 'price', 'condition', 'owned']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AccessoryUpdate(LoginRequiredMixin, UpdateView):
    model = Accessory
    fields = ['name', 'accessory_type', 'year', 'manufacturer', 'serial', 'price', 'condition', 'owned']

class AccessoryDelete(LoginRequiredMixin, DeleteView):
    model = Accessory
    success_url = '/collections/'
    
@login_required
def add_photo(request, instrument_id, accessory_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.session.Session(profile_name='gas-app').client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            if instrument_id > 0:
                photo = InstrumentPhoto(url=url, instrument_id=instrument_id)
            elif accessory_id > 0:
                photo = AccessoryPhoto(url=url, accessory_id=accessory_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    if instrument_id > 0:
        return redirect('instruments_detail', instrument_id=instrument_id)
    elif accessory_id > 0:
        return redirect('accessories_detail', accessory_id=accessory_id)

@login_required
def delete_photo(request, photo_id, instrument_id, accessory_id):
    if instrument_id > 0: 
        photo = InstrumentPhoto.objects.filter(id=photo_id)
        photo.delete()
        return redirect('instruments_detail', instrument_id=instrument_id)
    if accessory_id > 0: 
        photo = AccessoryPhoto.objects.filter(id=photo_id)
        photo.delete()
        return redirect('accessories_detail', accessory_id=accessory_id)
    
