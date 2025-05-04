from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order
from drf_yasg.utils import swagger_auto_schema


class ProductCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        # product = Product.objects.get(pk=pk)
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductByCategoryAPIView(APIView):
    def get(self, request, category_id):
        products = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class OrderListAPIView(APIView):
    def get(self, request):
        ordres = Order.objects.all()
        serializer = OrderSerializer(ordres, many=True)
        return Response(serializer.data)


class OrderByUserAPIView(APIView):
    def get(self, request, user_id):
        orders = Order.objects.filter(owner__id=user_id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
