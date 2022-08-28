from xml.etree.ElementInclude import include
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from . import views



urlpatterns = [ 
    # AUTHENTICATION API ENDPOINTS
    path('auth/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



    path('password-change/', views.ChangePasswordApiView.as_view(), name='password-reset'),
    path('password-reset/confirm/', views.SetNewPasswordApiView.as_view(), name='password-reset-confirm'),



    path('users/', views.UserListApiView.as_view()), 
    path('users/<int:pk>/', views.UserRetrieveUpdateDestroyApiView.as_view()),
    path('users/create/', views.UserCreateApiView.as_view()),


    path('discount/products/', views.ProductWithDiscountListApiView.as_view()),
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('search/products/', views.ProductSearchAPIView.as_view()),
    path('products/<int:pk>/likes/', views.like_product_view),
    path('products/<int:pk>/dislikes/', views.dislike_product_view),
    path('products/<int:pk>/', views.ProductDetailApiView.as_view()),

    path('company/', views.CompanyListCreateApiView.as_view()),
    path('company/<int:pk>/', views.CompanyDetailApiView.as_view()),
] 