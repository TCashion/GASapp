from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('collections/', views.index, name='index'),
    path('instruments/<int:instrument_id>/', views.instruments_detail, name='instruments_detail'),
    path('instruments/create', views.InstrumentCreate.as_view(), name='instruments_create'),
    path('instruments/<int:pk>/update', views.InstrumentUpdate.as_view(), name='instruments_update'),
    path('instruments/<int:pk>/delete', views.InstrumentDelete.as_view(), name='instruments_delete'),
    path('accessories/create', views.AccessoryCreate.as_view(), name='accessories_create'),
    path('accessories/<int:accessory_id>/', views.accessories_detail, name='accessories_detail'),
    path('accessories/<int:pk>/update', views.AccessoryUpdate.as_view(), name='accessories_update'),
    path('accessories/<int:pk>/delete', views.AccessoryDelete.as_view(), name='accessories_delete'),
]