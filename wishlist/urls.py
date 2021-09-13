from django.urls import path
from . import views

app_name='wishlist'

urlpatterns = [
    path('add/<uuid:product_id>/', views.add_wishlist, name='add_wishlist'),
    path('', views.wishlist_detail, name='wishlist_detail'),
    path('remove/<uuid:product_id>/', views.wishlist_remove, name='wishlist_remove'),
    path('wishlist_full_remove/<uuid:product_id>/', views.wishlist_full_remove, name='wishlist_full_remove'),
]