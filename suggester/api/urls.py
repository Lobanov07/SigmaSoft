from django.urls import path, include
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<int:product_id>/recommendations/', views.ProductRecommendationsAPIView.as_view(), name='product-recommendations'),
    path('products/popular/', views.PopularProductsAPIView.as_view(), name='popular-products'),

    path('session/create/', views.CreateSessionAPIView.as_view(), name='create-session'),
    path('interactions/', views.UserInteractionsAPIView.as_view(), name='user-interactions'),
    path('feedback/', views.FeedbackAPIView.as_view(), name='feedback'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]