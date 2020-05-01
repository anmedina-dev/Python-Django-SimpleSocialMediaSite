from django.shortcuts import render
from django.http import HttpResponse
from .models import Stock
from django.contrib.auth.models import User
import yfinance as yf

# Create your views here.
def index(request):
    return render(request, './blog/home.html')