from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('instruments/', views.instruments_index, name='instruments_index'),
    path('instruments/<int:instrument_id>/', views.instruments_detail, name='instruments_detail'),
    path('instruments/create', views.InstrumentCreate.as_view(), name='instruments_create'),
    path('instruments/<int:pk>/update', views.InstrumentUpdate.as_view(), name='instruments_update'),
    path('instruments/<int:pk>/delete', views.InstrumentDelete.as_view(), name='instruments_delete'),
]