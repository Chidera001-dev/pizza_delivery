from django.shortcuts import render, get_object_or_404
from rest_framework import generics , status
from rest_framework.response import Response
from . import serializers
from .models import Order
from drf_yasg.utils import swagger_auto_schema  
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.contrib.auth import get_user_model
User = get_user_model()



class HelloOrdersView(generics.GenericAPIView):
    @swagger_auto_schema(operation_summary="Hello Orders Endpoint")
    def get(self, request):
        return Response(data={"message": "Hello, orders!"},status=status.HTTP_200_OK)


class OrdercreateListView(generics.GenericAPIView):
    serializer_class = serializers.OrderCreationSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="List all orders made")
    def get(self, request):
        order = Order.objects.all()  
        serializer = self.serializer_class(instance=order, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create a new order")
    def post(self, request):
        data=request.data
        serializer = self.serializer_class(data=data)

        user=request.user

        if serializer.is_valid():
            serializer.save(customer=user)  
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class OrderDetailView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Retrieve an order by ID")
    def get(self, request, order_id):
        order=get_object_or_404(Order, pk=order_id)

        serializer = serializers.OrderCreationSerializer(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update an order by ID")
    def put(self, request, order_id):
        data=request.data

        order=get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Delete an order by ID")        
    def delete(self, request, order_id):
        order=get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(data={"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class UpdateOrderStatusView(generics.GenericAPIView):
    serializer_class = serializers.OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Update order status by ID")
    def put(self, request, order_id):
        data=request.data

        order=get_object_or_404(Order, pk=order_id)

        serializer = self.serializer_class(data=data, instance=order)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserOrdersView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="List all orders for a specific user")
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)  
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        orders = Order.objects.filter(customer=user)  
        serializer = self.serializer_class(instance=orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserOrderDetail(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Retrieve a specific order for a specific user")
    def get(self, request, user_id, order_id):
        
        user = User.objects.get(pk=user_id)  

        order=Order.objects.all().filter(customer=user).get(pk=order_id)

        serializer=self.serializer_class(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    


        
            
                
                
        
       
    

