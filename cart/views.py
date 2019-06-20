from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404,  HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from obp.models import Product
from .cart import Cart
import cgi

def CartAdd(request):
    product_id = request.GET.get('id')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id )
    cart.add(product)
    return JsonResponse({
        'id': product_id,
        'count': len(cart)
        })

def CartRemove(request):
    product_id = request.GET.get('id')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id )
    cart.remove(product)
    return JsonResponse({
        'totalPrice': cart.get_total_price(),
        'quantity': cart.__len__(),
        'count': len(cart)
        })

def MinusQuantity(request):
    product_id = request.GET.get('id')
    cart = Cart(request)
    if cart.cart[product_id]['quantity'] > 1:
        product = get_object_or_404(Product, id=product_id )
        cart.minus_quantity(product)

    return JsonResponse({
        'quantity': cart.cart[product_id]['quantity'],
        'totalPrice': cart.get_total_price(),
        'count': len(cart)
        })

def PlusQuantity(request):
    product_id = request.GET.get('id')
    cart = Cart(request)
    if cart.cart[product_id]['quantity'] < 20:
        product = get_object_or_404(Product, id=product_id )
        cart.plus_quantity(product)
    return JsonResponse({
        'quantity': cart.cart[product_id]['quantity'],
        'totalPrice': cart.get_total_price(),
        'count': len(cart)
        })


def RemoveProduct(request):
    product_id = request.GET.get('id')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id )
    cart.remove_product(product)
    return JsonResponse({
        'totalPrice': cart.get_total_price(),
        'quantity': cart.lena(),
        'count': len(cart)
        })


def CartList(request):
    cart = Cart(request)
    #if cart.getCartList():
    return JsonResponse({
    'cartList': cart.getCartList(),
    'totalPrice': cart.get_total_price()
    })

def CartCount(request):
    cart = Cart(request)
    return JsonResponse({'count': len(cart) })

    # return JsonResponse({
    # 'cartList': False
    # })

def CartDetail(request):
    cart = Cart(request)
    return render(request, 'obp/cart.html', {'cart': cart })
