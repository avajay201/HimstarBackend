from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import  User
from .models import BankDetail, WithdrawalRequest
from .serializers import BankDetailSerializer, WithdrawalRequestSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.models import Register


class BankDetailRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return BankDetail.objects.get(user__user__id=id)
        except BankDetail.DoesNotExist:
            return None

    def get(self, request):
        bank_detail = self.get_object(request.user.id)
        print('bank_detail>>>', bank_detail)
        if bank_detail:
            serializer = BankDetailSerializer(bank_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        register = Register.objects.filter(user=request.user).first()
        request.data['user'] = register.id
        serializer = BankDetailSerializer(data=request.data)
        print(request.data, '----------')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        bank_detail = self.get_object(request.user.id)
        if bank_detail:
            bank_detail.delete()
            return Response(status=status.HTTP_200_OK)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class WithdrawalRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        register_id = Register.objects.filter(user=request.user).first()
        withdrawals = WithdrawalRequest.objects.filter(user__user=request.user).order_by('-id')
        serializer = WithdrawalRequestSerializer(withdrawals, many=True)

        data =  {
            "withdrawal_history":serializer.data,
            "amount":  register_id.points
        }
        print(data, '-------------')
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # Get the Register object for the authenticated user
        register = Register.objects.filter(user=request.user).first()

        if not register:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add the user ID to the request data
        request.data['user'] = register.id  # Make sure this is correct

        # Get the amount from the withdrawal request
        amount = request.data.get('amount')

        if not amount:
            return Response({"detail": "Amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure that the amount is a positive value and cast it to a Decimal
            amount = float(amount)  # Convert amount to float

            # Check if the user has enough points
            if register.points < amount:
                return Response({"detail": "Insufficient points."}, status=status.HTTP_400_BAD_REQUEST)

            # Subtract the withdrawal amount from the user's points
            register.points -= amount
            register.save()

        except ValueError:
            return Response({"detail": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and save the withdrawal request
        serializer = WithdrawalRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=register)  # Ensure 'user' is passed explicitly to the serializer
            register_id = Register.objects.filter(user=request.user).first()
            withdrawals = WithdrawalRequest.objects.filter(user__user=request.user).order_by('-id')
            serializer = WithdrawalRequestSerializer(withdrawals, many=True)
            data = {
                "withdrawal_history": serializer.data,
                "amount": register_id.points
            }
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)