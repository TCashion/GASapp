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
    path('add_photo/<int:instrument_id>/<int:accessory_id>/', views.add_photo, name='add_photo'),
    path('delete_photo/<int:photo_id>/<int:instrument_id>/<int:accessory_id>/', views.delete_photo, name='delete_photo'),
    path('accessories/create', views.AccessoryCreate.as_view(), name='accessories_create'),
    path('accessories/<int:accessory_id>/', views.accessories_detail, name='accessories_detail'),
    path('accessories/<int:pk>/update', views.AccessoryUpdate.as_view(), name='accessories_update'),
    path('accessories/<int:pk>/delete', views.AccessoryDelete.as_view(), name='accessories_delete'),
    path('instruments/<int:instrument_id>/assoc_accessory/<int:accessory_id>/', views.assoc_accessory, name='assoc_accessory'),
    path('instruments/<int:instrument_id>/dis_assoc_accessory/<int:accessory_id>/', views.dis_assoc_accessory, name='dis_assoc_accessory'),
]
