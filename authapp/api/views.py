from rest_framework.decorators import api_view
from authapp.api.serializers import  RegistrationSerializer, ProfileSerializer, ProfileUpdateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from authapp import models
from authapp.models import Profile
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from rest_framework.views import APIView
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404

class LogoutView(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        return Response(status=status.HTTP_200_OK)
    
class SignUp(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            account = serializer.save()
            
            # Generate the access and refresh tokens for the new user
            refresh = RefreshToken.for_user(account)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            data['response'] = "Registration Successful"
            data['username'] = account.username
            data['email'] = account.email
            data['access_token'] = access_token
            data['refresh_token'] = refresh_token
            
        else:
            data = serializer.errors
            return Response(status=409)
        return Response(data)


class ProfileView(APIView):
    # authentication_classes = [JWTAuthentication]  # احراز هویت با JWT
    permission_classes = [IsAuthenticated]
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'username', openapi.IN_QUERY, description="Username of the user", type=openapi.TYPE_STRING
    #         )
    #     ]
    # )

    def get(self, request):
        # دریافت کاربر لاگین شده
        profile = get_object_or_404(Profile, user=request.user)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # def get(self, request):
    #     username = request.GET.get('username')  # گرفتن پارامتر از URL

    #     if not username:
    #         return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    #     user = get_object_or_404(User, username=username)  # پیدا کردن کاربر
    #     profile = get_object_or_404(Profile, user=user)  # پیدا کردن پروفایل کاربر

    #     serializer = ProfileSerializer(profile)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # def get(self, request):
    #     profiledata = Profile.objects.all()

    #     serializer = ProfileSerializer(profiledata, many=True)
    #     return Response(serializer.data)

    
    @swagger_auto_schema(request_body=ProfileUpdateSerializer)
    

    def put(self, request):
            # Get the username from the request body
            username = request.data.get('username')

            if not username:
                return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Get the User instance by username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise NotFound(f"User with username {username} not found")

            # Use ProfileUpdateSerializer for updating
            serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                # Save the updated data
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
       
    

