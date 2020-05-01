from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    amount = models.IntegerField()
    date_entered = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.ticker

#Redirect to the stock detail after stock is created
    def get_absolute_url(self):
       return reverse('stock-detail', kwargs={'pk': self.pk})