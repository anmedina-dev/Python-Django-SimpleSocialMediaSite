from django.urls import path
from . import views
from .views import (StockCreateView,
                    StockListView,
                    StockDetailView,
                    StockDeleteView,
                    StockUpdateView,
                    UserStockListView)

urlpatterns = [
    path('', StockListView.as_view(), name='data'),
    path('user/<str:username>', UserStockListView.as_view(), name='user-stocks'),
    path('stock/<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
    path('stock/<int:pk>/update.', StockUpdateView.as_view(), name='stock-update'),
    path('stock/<int:pk>/delete/', StockDeleteView.as_view(), name='stock-delete'),
    path('newStock/', StockCreateView.as_view(), name='stock-create'),
]