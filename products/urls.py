from django.urls import path

from .views import (
                        ProductListView, 
                        ProductDetailSlugView,
                    )

urlpatterns = [
    path('', ProductListView.as_view()),
    path('<slug:slug>/', ProductDetailSlugView.as_view()),
    path('products-fbv/', product_list_view), 
    path('products/<int:pk>', ProductDetailView.as_view()),
    path('products-fbv/<int:pk>', product_detail_view), 
    path('products/<slug:slug>/', ProductDetailSlugView.as_view()),
    path('featured/', ProductFeaturedListView.as_view()),
    path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
]