from django.urls import path
from.import views


urlpatterns = [
    path('', views.view_basket, name='view_basket'),
    path('add_to_basket/<product_id>/', views.add_to_basket, name='add_to_basket'),
    path('update/<int:product_id>/', views.update_basket, name='update_basket'),
    path('remove/<int:product_id>/', views.remove_basket, name='remove_basket'),
    path('remove_whole_basket/', views.remove_whole_basket, name='remove_whole_basket'), 
]