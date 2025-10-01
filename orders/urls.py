from django.urls import path
from . import views


urlpatterns =[
    path('',views.OrdercreateListView.as_view(), name='orders' ),
    path('<int:order_id>/',views.OrderDetailView.as_view(), name='order-detail' ),
    path('update-status/<int:order_id>/',views.OrderDetailView.as_view(), name='order-status-update' ),
    path('user/<int:user_id>/orders/',views.UserOrdersView.as_view(), name='user_orders' ),
    path('user/<int:user_id>/order/<int:order_id>',views.UserOrderDetail.as_view(), name='user_specific_details' ),
]

