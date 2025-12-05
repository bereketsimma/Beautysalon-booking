from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer

class CustomerRegisterSerializer(serializers.ModelSerializer):
    # Fields from the linked User model
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source='user.password', write_only=True)

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'phone', 'email_address']  # include Customer fields

    def create(self, validated_data):
        # Extract the user data
        user_data = validated_data.pop('user')
        
        # Create the User first
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )

        # Create the linked Customer
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
