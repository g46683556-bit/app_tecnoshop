from django.shortcuts import render
from catalog.models import Catalog
import random

def home(request):
    todos = list(Catalog.objects.all())
    productos_destacados = random.sample(todos, min(len(todos), 4))  # hasta 6 al azar
    return render(request, "pages/home.html", {"productos": productos_destacados})

def contact_us(request):
    return render(request, "pages/contact_us.html")