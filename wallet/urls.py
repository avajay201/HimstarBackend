from django.urls import path
from .views import UserBankDetailView,AllWithdrawalRequestsView,UserWithdrawalRequestsView

urlpatterns = [
    path('bank-details/', UserBankDetailView.as_view(), name='bank-details'),
    path('withdrawals/all/', AllWithdrawalRequestsView.as_view(), name='all-withdrawals'),
    path('withdrawals/', UserWithdrawalRequestsView.as_view(), name='user-withdrawals'),
]
