from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Income, Expenditure
from .serializers import IncomeSerializer, ExpenditureSerializer, UserSerializer, LoginSerializer
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.authentication import TokenAuthentication


# Signup View
class SignupView(APIView):
    
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @extend_schema(
        tags=["user"],  
        description="This endpoint is used to create a user using a valid email and password.",
        summary="Register User"
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        tags=["user"],  
        description="This endpoint is used to log a user in.",
        summary="Logs user into the system",
        request=LoginSerializer
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Logout view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = None

    @extend_schema(
        tags=["user"],  
        description="This endpoint invalidates the refresh token and kills the user sesion.",
        summary="Logs out the current logged-in user.",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "refresh": {
                        "type": "string",
                        "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVza"
                    }
                },
                "required": ["refresh"]
            }
        }
    )
    
    def post(self, request):
        if request.user and request.auth:
            request.auth.delete()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_400_BAD_REQUEST)

# Userprofile view
@extend_schema_view(
        get=extend_schema(tags=["user"], description="Get user by user ID.", summary="Get user by user ID"),
        put=extend_schema(tags=["user"], description="This can only be done by the logged in user.", summary="Update user profile"),
    )    
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete', 'post']

    def get_object(self):
        return self.request.user

# Income List View
@extend_schema_view(
        get=extend_schema(tags=["income"], description="This endpoint returns the user's income.", summary="Get user's income data"),
        post=extend_schema(tags=["income"], description="This endpoint allows you to add an income.", summary="Add income data")
    )
class IncomeListView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete', 'post']

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Income Detail View
@extend_schema_view(
        get=extend_schema(tags=["income"], description="Get income data by ID.", summary="Get income data by ID"),
        put=extend_schema(tags=["income"], description="Update income data by ID.", summary="Update income data by ID"),
        delete=extend_schema(tags=["income"], description="Delete income data by ID.", summary="Delete income data by ID")
    )
class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete', 'post']

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

# Expenditure List View
@extend_schema_view(
        get=extend_schema(tags=["expenditure"], description="This endpoint returns the user's expenditure", summary="Get user's expenditure data."),
        post=extend_schema(tags=["expenditure"], description="This endpoint allows you to add an expenditure", summary="Add expenditure data.")
    )
class ExpenditureListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenditureSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete', 'post']

    def get_queryset(self):
        return Expenditure.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Expenditure Detail View
@extend_schema_view(
        get=extend_schema(tags=["expenditure"], description="Get expenditure data by ID.", summary="Get expenditure data by ID."),
        put=extend_schema(tags=["expenditure"], description="Update expenditure data by ID.", summary="Update expenditure data by ID."),
        delete=extend_schema(tags=["expenditure"], description="Delete expenditure data by ID.", summary="Delete expenditure data by ID.")
    )
class ExpenditureDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenditureSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'delete', 'post']

    def get_queryset(self):
        return Expenditure.objects.filter(user=self.request.user)

    