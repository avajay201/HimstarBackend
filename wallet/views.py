from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import BankDetail,WithdrawalRequest
from .serializers import BankDetailSerializer,WithdrawalRequestSerializer


class UserBankDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            bank_detail = BankDetail.objects.get(user=request.user)
            serializer = BankDetailSerializer(bank_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BankDetail.DoesNotExist:
            return Response({"error": "Bank details not found"}, status=status.HTTP_404_NOT_FOUND)
        


class AllWithdrawalRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:  # Allow only staff/admins to access
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        withdrawal_requests = WithdrawalRequest.objects.all()
        serializer = WithdrawalRequestSerializer(withdrawal_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserWithdrawalRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        withdrawal_requests = WithdrawalRequest.objects.filter(user=request.user)
        serializer = WithdrawalRequestSerializer(withdrawal_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

