from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('<int:product_id>/', views.product_details, name='product_details'), 
    path('woman_products/', views.woman_products, name='woman_products'),
    path('man_products/', views.man_products, name='man_products'),
    path('kids_products/', views.kids_products, name='kids_products'),
]