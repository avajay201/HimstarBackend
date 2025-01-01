import hashlib
from rest_framework import status
import uuid
from accounts.models import  Register
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PaymentSerializer
from video.serializers import ParticipantSerializer
import requests
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from payments.models import PaymentDetails




class PaymentCreateGetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print('request.data>>>>', request.data)
        competition = request.data.get('competition')
        user = request.user.id
        print('request.user.id>>>>', request.user.id)
        # request.data['user'] = request.user.id
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            participate_serializer = ParticipantSerializer(data=request.data)
            if participate_serializer.is_valid():
                participate_serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors, '111111111111111111111111')
                Response(participate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors, '222222222222222222222222')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = Register.objects.filter(user=request.user).first()
        payments = PaymentDetails.objects.filter(user=user)
        payments_serializer = PaymentSerializer(payments, many=True)
        return Response(payments_serializer.data, status=status.HTTP_200_OK)
    

    
@csrf_exempt
def successview(request):
    return render(request, 'success.html')


@csrf_exempt
def failure(request):
    return render(request, 'failure.html')





