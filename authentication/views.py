from django.shortcuts import render
from rest_framework import generics , status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import UserCreationSerializer



class HelloAuthView(generics.GenericAPIView):
    @swagger_auto_schema(operation_summary="Hello Auth Endpoint")
    def get(self, request):
        return Response(data={"message": "Hello, Auth!"},status=status.HTTP_200_OK)


class UserCreateView(generics.GenericAPIView):
    serializer_class = UserCreationSerializer

    @swagger_auto_schema(operation_summary="Create a user account")
    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 












# Create your views here.
