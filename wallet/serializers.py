from rest_framework import serializers
from .models import BankDetail,WithdrawalRequest

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = ['account_holder_name', 'bank_name', 'account_number', 'ifsc_code', 'branch_name', 'created_at', 'updated_at']


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = ['id', 'user', 'amount', 'status', 'requested_at', 'processed_at']