from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    # validate method will check the similarity of password & confirm_password
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match'
            })

        return attrs

    def create(self, validated_data):
        # remove the confirm_password field as it's not a User model field
        validated_data.pop('confirm_password')

        # create user based on validated_data and hash the password

        # here User.objects.create_user() method is used instead of User.objects.create()
        # because create_user() can hash the password 
        user = User.objects.create_user(**validated_data)

        # return the created object
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }

        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'dob', 'address']
        read_only_fields = ['id', 'email']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                "Your current password is incorrect."
            )
        return value

    def validate_new_password(self,value):
        validate_password(value, user = self.context['request'].user)
        return value

    def validate(self, attrs):
        old_password = attrs['old_password']
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']

        if old_password == new_password:
            raise serializers.ValidationError({
                'new_password': "New password cannot be the same as the old password."
            })
        if new_password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match'
            })
        return attrs