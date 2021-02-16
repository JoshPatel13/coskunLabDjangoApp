from django.urls import path
from . import views

urlpatterns = [
    path('get-latest/', views.get_latest, name='get-latest'),
    path('get-livestreams/', views.get_livestreams, name='get-livestreams'),
    path('add-livestream/', views.add_livestream, name='add-livestream'),
    path('delete-livestream/<int:id>/', views.delete_livestream, name='delete-livestream')
]
