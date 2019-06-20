"""diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.conf.urls import include
from django.contrib import admin
from django.conf.urls import handler404

from . import views



app_name = 'obp'
urlpatterns = [
    #Главная страница
    path('', views.main_page, name = "main_page"),

    #Страница выбора товаров
    re_path('product-category-(?P<pk>[0-9]+)/', views.ProductsView.products_page, name="products_page"),
    path('search/', views.ProductsView.search, name = "search"),
    path('stocks/', views.ProductsView.stocks, name = "stocks"),




        #Страница товара
    re_path('product-(?P<pk>[0-9]+)/', views.product_page, name="product_page"),

    #Страница оформления заказа
    re_path('checkout/', views.checkout_page, name = "checkout"),

    re_path('checkout_success/', views.checkout_success_page, name = "cs"),

    path('checkout_issue_delivery/', views.CheckoutView.issue_delivery, name = "issue_delivery"),
    path('checkout_issue_pickup/', views.CheckoutView.issue_pickup, name = "issue_pickup"),


    path('authorization', views.auth, name = "auth"),
    path('addComment-Product(?P<product>[0-9]+)-Client-(?P<client>[0-9]+)', views.ProductView.addComment, name = "addComment"),
    path('addRating/', views.ProductView.addRating, name = "addRating"),



    path('login', views.Authorization.login, name = "login"),
    path('logout/', views.Authorization.logout, name = "logout"),
    path('personal_account', views.Authorization.personal_account, name = "personal_account"),
    path('get_code', views.Authorization.get_code, name = "get_code"),
    path('change_client', views.Authorization.change_client, name = "change_client"),

    path('delivery-cost/', views.DeliveryCost.get_delivery_cost, name = "get_delivery_cost"),
    path('pickup-cost/', views.DeliveryCost.get_pickup_cost, name = "get_pickup_cost"),


    path('about-us/', views.OtherView.about_us, name = "about_us"),
    path('contacts/', views.OtherView.contacts, name = "contacts"),
    path('express/', views.OtherView.express, name = "express"),

    path('error/', views.OtherView.error_page, name = "error"),
]
