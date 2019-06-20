from django.urls import path, re_path
from . import views

app_name = 'cart'
urlpatterns = [
    path('add/', views.CartAdd, name='CartAdd'),
    path('remove/', views.CartRemove, name='CartRemove'),
    path('minus_quantity/', views.MinusQuantity, name='MinusQuantity'),
    path('plus_quantity/', views.PlusQuantity, name='PlusQuantity'),
    path('remove_product/', views.RemoveProduct, name='RemoveProduct'),
    path('detail/', views.CartDetail, name = 'cartDetail'),
    path('CartList/', views.CartList, name = 'CartList'),
    path('CartCount/', views.CartCount, name = 'CartCount'),
]
