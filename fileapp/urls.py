from django.urls import path
from .views import fileapp_view

urlpatterns = [
    path('', fileapp_view, name='file')
]
