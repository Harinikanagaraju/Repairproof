from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path(
        'add-appliance/',
        views.add_appliance,
        name='add_appliance'
    ),

    path(
        'delete-appliance/<int:pk>/',
        views.delete_appliance,
        name='delete_appliance'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),
]