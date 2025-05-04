from django.urls import path
from .views import (
    ProductCreateAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ProductByCategoryAPIView,
    OrderListAPIView,
    OrderByUserAPIView,
    OrderCreateAPIView,
)

app_name = "products"

urlpatterns = [
    path("create/", ProductCreateAPIView.as_view(), name="product_create"),
    path("list/", ProductListAPIView.as_view(), name="product_list"),
    path("detail/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path("category/<int:category_id>/", ProductByCategoryAPIView.as_view(), name="products_category"),
    path("orders/", OrderListAPIView.as_view(), name="order_list"),
    path("owner/<int:user_id>/", OrderByUserAPIView.as_view(), name="order_user"),
    path("order/", OrderCreateAPIView.as_view(), name="order_create"),

]
