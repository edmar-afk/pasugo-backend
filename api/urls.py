from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
# ssd
urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('profiles/role/<str:role>/', views.ProfileByRoleView.as_view(), name='profiles-by-role'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
    path('clients/', views.ClientsListView.as_view(), name='clients-list'),
    
    
    path('post-products/', views.ProductCreateView.as_view(), name='product-list-create'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('edit-product/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('delete-product/<int:id>/', views.ProductDeleteView.as_view(), name='delete-product'),
    path('product-details/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    
    path('deliveries/submit/<int:user_id>/<int:product_id>/', views.SubmitDeliveryView.as_view(), name='submit-delivery'),
    path('deliveries/user/<int:user_id>/', views.UserDeliveriesView.as_view(), name='user-deliveries'),
    path('deliveries/', views.DeliveryListView.as_view(), name='delivery-list'),
    path('deliveries/<int:delivery_id>/update-status/', views.UpdateDeliveryStatusView.as_view(), name='update-delivery-status'),
    path("deliveries/<int:delivery_id>/delete/", views.DeleteDeliveryView.as_view(), name="delete-delivery"),
    path("deliveries/<int:delivery_id>/payment/", views.UpdateDeliveryPaymentView.as_view(), name="update_delivery_payment"),
    
    path('riders/', views.RidersListView.as_view(), name='riders-list'),
    path('users/<int:user_id>/update-status/', views.UpdateUserStatusView.as_view(), name='update-user-status'),
    path('users/<int:userid>/delete/', views.DeleteUserView.as_view(), name='delete-user'),
    
    
    path('transportation/<int:user_id>/create/', views.TransportationCreateView.as_view(), name='transportation-create'),
    path('transportations/<int:customer_id>/', views.CustomerTransportationListView.as_view(), name='customer-transportations'),
    path('transport-map/<int:transportation_id>/', views.TransportMapView.as_view(), name='transport-map'),
    path('transportations/<int:transportation_id>/update-price-payment/', 
         views.TransportationUpdatePricePaymentView.as_view(), 
         name='update-price-payment'),
    
    path('transports/', views.TransportationListView.as_view(), name='transport-list'),
    path('transport/<int:transport_id>/update/', views.UpdateTransportView.as_view(), name='update-transport'),
    path('transport/<int:transport_id>/payment/', views.TransportationPaymentView.as_view(), name='transport-payment'),
    
    
    
    path('deliveries/arrived/', views.ArrivedDeliveryListView.as_view(), name='arrived-deliveries'),
    path('transportations/arrived/', views.ArrivedTransportationListView.as_view(), name='arrived-transportations'),
    
    
    
    path('chat/<int:user1_id>/<int:user2_id>/', views.ChatRoomView.as_view(), name='chat-room'),
    path('chat/users/<int:user_id>/', views.UserRoomsView.as_view(), name='user-rooms'),
    path("chat-user/<str:first_name>/", views.ChatUserView.as_view(), name="chat-user"),
    
    
     path(
        "products/<int:product_id>/deduct-quantity/",
        views.DeductProductQuantityView.as_view()
    ),
    
]
