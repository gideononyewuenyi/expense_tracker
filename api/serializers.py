from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Income, Expenditure
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

# User Serializer
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Signup Example',
            value={
                "first_name": "John",
                "last_name": "Doe",
                "username": "john_doe",
                "email": "john@email.com",
                "password": "12345"
            },
            request_only=True,  
            response_only=False,  
        )
    ]
)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # this will prevent password from being exposed
        }


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),  
            last_name=validated_data.get('last_name', ''),    
            password=validated_data['password']
        )
        return user
    

# Login Serializer
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Login Example',
            value={
                "username": "john_doe",
                "password": "12345"
            },
            request_only=True,  
            response_only=False,  
        )
    ]
)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

# Income Serializer
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Create Income Example",
            summary="Example payload for creating an income",
            description="Payload example for adding a new income entry.",
            value={
                "title": "Salary",
                "amount": "5000.00",
                "description": "Payment for my November salary.",
                "date_added": "2024-11-20"
            },
        ),
    ]
)
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'user', 'title', 'amount', 'description', 'date_added']
        read_only_fields = ['user', 'date_added']


# Expenditure Serializer
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Create Expenditure Example",
            summary="Example payload for creating an expenditure",
            description="Payload example for adding a new expenditure entry.",
            value={
                "title": "Transport",
                "amount": "2000.00",
                "date": "2024-11-20",
                "description": "Transportation bill for November."
            },
        ),
    ]
)
class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenditure
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
