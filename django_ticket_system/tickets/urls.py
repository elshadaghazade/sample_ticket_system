from django.urls import path
from .views import BuyTicketView

urlpatterns = [
    path('', BuyTicketView.as_view(), name='buy_ticket')
]
