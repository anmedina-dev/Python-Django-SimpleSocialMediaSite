from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView,
                                DetailView, 
                                CreateView,
                                UpdateView,
                                DeleteView)
from django.http import HttpResponse
from .models import Stock
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import yfinance as yf
import numpy as np
import pandas as pd

# Create your views here.
def index(request):
    context = {
        #Stock.objects.all() is a database query to get all the posts
        'stock': Stock.objects.all()
    }
    #the context is the posts from the database
    return render(request, './data/data_home.html', context)

class StockListView(ListView):
    model = Stock
    template_name = 'data/data_home.html'
    context_object_name = 'stocks'
    ordering = ['-date_entered']
    paginate_by = 5

class StockDetailView(DetailView):
    model = Stock

#posts from a specific user
class UserStockListView(ListView):
    model = Stock
    template_name = 'data/user_stocks.html'
    context_object_name = 'stocks'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Stock.objects.filter(owner=user).order_by('-date_entered')
        
class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    fields = ['ticker', 'amount']

    #makes the current logged user the owner of post
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

#Mixins have to be to the left of the View
class StockUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Stock
    fields = ['ticker', 'amount']

    #makes the current logged user the owner of post
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        stock = self.get_object()
        if self.request.user == stock.owner:
            return True
        return False


class StockDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Stock
    success_url = '/'

    def test_func(self):
        stock = self.get_object()
        if self.request.user == stock.owner:
            return True
        return False