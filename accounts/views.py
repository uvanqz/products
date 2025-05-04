from rest_framework.views import APIView
from accounts.serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


class UserRegistrationAPIView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        selializer = UserSerializer(data=request.data)
        if selializer.is_valid():
            selializer.save()
            return Response(selializer.data, status=status.HTTP_201_CREATED)
        return Response(selializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response(
                {"message": "Успешная авторизация"}, status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Ошибка авторизации"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Успешный выход"}, status=status.HTTP_200_OK)

    def get(self, request):
        logout(request)
        return Response({"message": "Успешный выход"}, status=status.HTTP_200_OK)
