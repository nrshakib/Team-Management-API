from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.serializers import CustomTokenObtainPairSerializer, UserProfileSerializer, UserRegistrationSerializer
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

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # self.get_serializer to receive login input data from request
        serializer = self.get_serializer(data = request.data)
        # is_valid checks credentials and creates token
        serializer.is_valid(raise_exception = True)

        return api_response(
            message = 'Login Successful',
            status_text="Success",
            data = serializer.validated_data, # tokens and data will be in the validated_data
            http_status= status.HTTP_200_OK,
        )

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # here request finds the user from token,so filtering is not necessary
        user = request.user
        serializer = UserProfileSerializer(user)

        return api_response(
            message = "Profile retrieved successfully",
            status_text="Success",
            data=serializer.data,
            http_status=status.HTTP_200_OK,
        )