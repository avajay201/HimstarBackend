from django.urls import path
from .views import BankDetailRetrieveUpdateDestroyAPIView, WithdrawalRequestAPIView

urlpatterns = [
    path('bankdetails/', BankDetailRetrieveUpdateDestroyAPIView.as_view(), name='bankdetail-retrieve-update-destroy'),
    path('withdrawal/', WithdrawalRequestAPIView.as_view(), name='withdrawal-api'),
]
