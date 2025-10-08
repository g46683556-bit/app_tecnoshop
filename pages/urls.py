from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contact_us/', contact_us, name='contact_us'),
]