from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Instrument, Accessory

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
    fields = ['name', 'instrument_type', 'year', 'manufacturer', 'serial', 'price', 'condition']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class InstrumentUpdate(LoginRequiredMixin, UpdateView):
    model = Instrument
    fields = ['name', 'instrument_type', 'year', 'manufacturer', 'serial', 'price', 'condition']
    
class InstrumentDelete(LoginRequiredMixin, DeleteView):
    model = Instrument
    success_url = '/instruments/'

class AccessoryCreate(LoginRequiredMixin, CreateView):
    model = Accessory
    fields = ['name', 'accessory_type', 'year', 'manufacturer', 'serial', 'price', 'condition']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AccessoryUpdate(LoginRequiredMixin, UpdateView):
    model = Accessory
    fields = ['name', 'accessory_type', 'year', 'manufacturer', 'serial', 'price', 'condition']