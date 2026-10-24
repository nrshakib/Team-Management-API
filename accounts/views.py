from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from accounts.serializers import UserRegistrationSerializer
from utils.utils import api_response

# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return api_response(
                message = "User registered succesfully.",
                status_text = "Success",
                data = {
                    "username": user.username,
                    "email": user.email
                },
                http_status= status.HTTP_201_CREATED
            )