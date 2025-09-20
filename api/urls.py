from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
# ssd
urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
    path('clients/', views.ClientsListView.as_view(), name='clients-list'),
    
    path('post-products/', views.ProductCreateView.as_view(), name='product-list-create'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('edit-product/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('delete-product/<int:id>/', views.ProductDeleteView.as_view(), name='delete-product'),
    path('product-details/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    path('deliveries/submit/<int:user_id>/<int:product_id>/', views.SubmitDeliveryView.as_view(), name='submit-delivery'),
    path('deliveries/user/<int:user_id>/', views.UserDeliveriesView.as_view(), name='user-deliveries'),
]
