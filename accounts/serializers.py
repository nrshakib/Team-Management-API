from rest_framework import serializers
from accounts.models import User

class UserRegistrationSerialiser(serializers.ModelSerializer):
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