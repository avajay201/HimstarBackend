from django.contrib import admin
from .models import BankDetail, WithdrawalRequest

admin.site.register(BankDetail)
admin.site.register(WithdrawalRequest)
