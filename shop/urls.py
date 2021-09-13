from django.urls import path
from . import views


app_name='shop'

urlpatterns = [
    path('', views.allProdCat, name='allProdCat'),
    path('<uuid:category_id>/', views.allProdCat, name='products_by_category'),
    path('<uuid:category_id>/<uuid:product_id>/', views.prod_details, name='prod_details'),
    path('<uuid:pk>/review/', views.add_product_review, name='add_product_review'),
]