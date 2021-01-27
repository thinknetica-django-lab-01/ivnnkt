from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Product


def index(request):
    prod = Product.objects.all()
    user = User.objects.filter(logentry = True)
    turn_on_block = True
    return render(request, 'main/index.html', {'prod': prod, 'user': user, 'turn_on_block': turn_on_block })



# Create your views here.
