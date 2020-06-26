from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Instrument, Accessory, InstrumentPhoto, AccessoryPhoto
import uuid
import boto3
import requests

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'gas-app'


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
    accessories = Accessory.objects.exclude(id__in=instrument.accessories.all().values_list('id')).filter(user=request.user)
    if instrument.owned == True:
        url = reverb(instrument)
        headers = {
            'content-type': 'application/hal+json',
            'accept': 'application/hal+json',
            'accept-version': '3.0'
            }
        r = requests.get(url, headers=headers)
        response = r.json()
        if 'estimated_value' in response['price_guides'][0]:
            low = response['price_guides'][0]['estimated_value']['price_low']['amount']
            high = response['price_guides'][0]['estimated_value']['price_high']['amount']
        else:
            low = None
            high = None
        price_guide = {
            'title': response['price_guides'][0]['title'],
            'low': low,
            'high': high,
            'url': response['price_guides'][0]['_links']['web']['href']
        }
        return render(request, 'instruments/detail.html', {
            'instrument': instrument,
            'accessories': accessories,
            'price_guide': price_guide,
        })
    else:
        url_wishlist = reverb_wishlist(instrument)
        headers = {
            'content-type': 'application/hal+json',
            'accept': 'application/hal+json',
            'accept-version': '3.0'            
        }
        r = requests.get(url_wishlist, headers=headers)
        response = r.json()
        if len(response['listings']) > 0:
            listing = response['listings'][0]['_links']['web']['href']
        else: 
            listing = None
        return render(request, 'instruments/detail.html', {
            'instrument': instrument,
            'accessories': accessories,
            'listing': listing,
        })


@login_required
def accessories_detail(request, accessory_id):
    accessory = Accessory.objects.get(id=accessory_id)
    url = reverb(accessory)
    headers = {
        'content-type': 'application/hal+json',
        'accept': 'application/hal+json',
        'accept-version': '3.0'
    }
    r = requests.get(url, headers=headers)
    response = r.json()
    if 'estimated_value' in response['price_guides'][0]:
        low = response['price_guides'][0]['estimated_value']['price_low']['amount']
        high = response['price_guides'][0]['estimated_value']['price_high']['amount']
    else:
        low = None
        high = None
    price_guide = {
        'title': response['price_guides'][0]['title'],
        'low': low,
        'high': high,
        'url': response['price_guides'][0]['_links']['web']['href']
    }
    return render(request, 'accessories/detail.html', {
        'accessory': accessory,
        'price_guide': price_guide,
    })


@login_required
def add_photo(request, instrument_id, accessory_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        # s3 = boto3.session.Session(profile_name='gas-app').client('s3')
        s3 = boto3.client('s3')
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


@login_required
def assoc_accessory(request, instrument_id, accessory_id):
    Instrument.objects.get(id=instrument_id).accessories.add(accessory_id)
    return redirect('instruments_detail', instrument_id=instrument_id)


@login_required
def dis_assoc_accessory(request, instrument_id, accessory_id):
    Instrument.objects.get(id=instrument_id).accessories.remove(accessory_id)
    return redirect('instruments_detail', instrument_id=instrument_id)


@login_required
def reverb(item):
    base_url = 'https://api.reverb.com/api/priceguide?query='
    name = item.name.replace(' ', '+')
    manufacturer = item.manufacturer.replace(' ', '+')
    year = str(item.year)
    complete_url = base_url + year + '+' + manufacturer + '+' + name
    return complete_url


@login_required
def reverb_wishlist(item):
    base_url = 'https://api.reverb.com/api/listings?query='
    name = item.name.replace(' ', '+')
    manufacturer = item.manufacturer.replace(' ', '+')
    year = str(item.year)
    if year == 'None':
        complete_url = base_url + '+' + manufacturer + '+' + name
    else:
        complete_url = base_url + year + '+' + manufacturer + '+' + name
    return complete_url


class InstrumentCreate(LoginRequiredMixin, CreateView):
    model = Instrument
    fields = ['name', 'instrument_type', 'year', 'manufacturer', 'serial', 'condition', 'owned']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class InstrumentUpdate(LoginRequiredMixin, UpdateView):
    model = Instrument
    fields = ['name', 'instrument_type', 'year', 'manufacturer', 'serial', 'condition', 'owned']


class InstrumentDelete(LoginRequiredMixin, DeleteView):
    model = Instrument
    success_url = '/collections/'


class AccessoryCreate(LoginRequiredMixin, CreateView):
    model = Accessory
    fields = ['name', 'accessory_type', 'year', 'manufacturer', 'serial', 'condition', 'owned']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccessoryUpdate(LoginRequiredMixin, UpdateView):
    model = Accessory
    fields = ['name', 'accessory_type', 'year', 'manufacturer', 'serial', 'condition', 'owned']


class AccessoryDelete(LoginRequiredMixin, DeleteView):
    model = Accessory
    success_url = '/collections/'
