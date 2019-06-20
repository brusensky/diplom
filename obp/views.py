from django.shortcuts import render, get_object_or_404, reverse
from django.http import  HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context, loader
from obp.models import *
from obp.forms import *
from cart.cart import Cart
from .auth import Auth

from jinja2 import Template
import datetime
import re

class ProductsView():
    @staticmethod
    def __get_stock_products():
        stocks = Stock.objects.filter(status = True)
        dict_stock = {}

        for stock_item in stocks:
            product_object = Product.objects.get(id = stock_item.product_id.id)
            dict_stock.update({
                product_object.title: stock_item.value
            })
        return dict_stock

    @staticmethod
    def __get_stock_products_object():
        stocks = Stock.objects.filter(status = True)
        dict_stock = []

        for stock_item in stocks:
            product_object = Product.objects.get(id = stock_item.product_id.id)
            dict_stock.append(product_object)
        return dict_stock


    def search(request):
        if request.method == "GET":
            cart = Cart(request)

            search_str = request.GET.get('search')
            product_found_objects = Product.objects.filter(title__icontains = search_str)

            return render(request, 'products-search.html', {
                'products': product_found_objects,
                'search_str': search_str,
                'cartList': cart.getCartListId(),
                'stocks': ProductsView.__get_stock_products(),
                'auth': Auth(request)
                })

    def products_page(request, pk, **kwargs):
        cart = Cart(request)

        return render(request, 'products-page.html', {
            'products': Product.objects.filter(section_id = pk),
            'section': Section.objects.get(id = pk),
            'cartList': cart.getCartListId(),
            'stocks': ProductsView.__get_stock_products(),
            'auth': Auth(request)
            })

    def stocks(request):
        cart = Cart(request)
        stocks = ProductsView.__get_stock_products_object()
        print(stocks)

        return render(request, 'products-page.html', {
            'products': stocks,
            'cartList': cart.getCartListId(),
            'stocks': ProductsView.__get_stock_products(),
            'auth': Auth(request)
            })

def main_page(request):
    return render(request, 'main.html', {
        'special_offers': Special_offers.objects.all(),
        'recommendations': Product.objects.all()[:10],
        'auth': Auth(request)
    })

def product_page(request, pk):
    cart = Cart(request)
    product_object = Product.objects.get(id = pk)
    auth = Auth(request)
    if auth.is_authorization():
        try:
            client_object = auth.get_client_object()
            rating = get_object_or_404(Product_rating, product = product_object, client = client_object)
            rating = rating.rating
        except:
            rating = 0
    else:
        rating = 0

    return render (request, 'product.html', {
        'product': product_object,
        'cartList': cart.getCartListId(),
        'other': Product.objects.filter(section_id = product_object.section_id ).exclude(id = pk),
        'auth': auth,
        'comment_form': Comment_form(),
        'rating': rating,
        'average_rating': product_object.get_average_rating()
    } )


def checkout_page(request):
    try:
        cart = Cart(request)
        return render(request, 'checkout.html', {
            'form_order': checkout_form_order(),
            'form_client': checkout_form_client(),
            'cart': cart,
            'auth': Auth(request)
        })
    except:
        return OtherView.error_page(request)


class CheckoutView():
    def __get_client_object(phone_number):
        try:
            obj = get_object_or_404(Client, phone_number = phone_number)
        except:
            obj = Client()
        return obj

    def issue_delivery(request):
        if request.method == 'POST':
            #print(3)
            name = request.POST.get("name")
            phone_number = request.POST.get("phone_number")

            reg = re.compile('[^0-9]')
            phone_number = reg.sub('', phone_number)

            email = request.POST.get("email")
            city = request.POST.get("city")
            street = request.POST.get("street")
            house = request.POST.get("house")
            entrance = request.POST.get("entrance")
            apartament_number = request.POST.get("apartament_number")

            client_object = CheckoutView.__get_client_object(phone_number)
            client_object.name = name
            client_object.email = email
            client_object.phone_number = phone_number
            client_object.save()

            cart = Cart(request)
            order_object = Order()

            order_object.client_id = client_object
            order_object.dateTimeOrder = datetime.datetime.now()
            order_object.price = str( cart.get_total_price() );
            order_object.city = city
            order_object.street = street
            order_object.house = house
            order_object.entrance = entrance
            order_object.apartament_number = apartament_number

            order_object.deliveryCost = str( DeliveryCost.get_delivery(request) );
            order_object.save()


            for cart_item in cart.cart:
                product_order = Product_order()
                product_order.product_id = get_object_or_404(Product, id = int(cart_item) )
                product_order.quantity = int ( cart.cart[cart_item]['quantity'] )
                product_order.order_id = order_object
                product_order.save()

            cart.clear()
            return JsonResponse({
                "result": "1"
            })
        else:
            return False


    def issue_pickup(request):
        if request.method == 'POST':
            #print(3)
            name = request.POST.get("name")
            phone_number = request.POST.get("phone_number")

            reg = re.compile('[^0-9]')
            phone_number = reg.sub('', phone_number)

            email = request.POST.get("email")

            client_object = CheckoutView.__get_client_object(phone_number)
            client_object.name = name
            client_object.email = email
            client_object.phone_number = phone_number
            client_object.save()

            cart = Cart(request)
            order_object = Order()

            order_object.client_id = client_object
            order_object.dateTimeOrder = datetime.datetime.now()
            order_object.price = str( cart.get_total_price() );
            order_object.deliveryCost = str( DeliveryCost.get_pickup(request) );

            order_object.save()

            for cart_item in cart.cart:
                product_order = Product_order()
                product_order.product_id = get_object_or_404(Product, id = int(cart_item) )
                product_order.quantity = int ( cart.cart[cart_item]['quantity'] )
                product_order.order_id = order_object
                product_order.save()

            cart.clear()
            return JsonResponse({
                "result": "1"
            })
        else:
            return False

def checkout_success_page(request):
    if request.method == 'POST':

        form = checkout_form(request.POST)
        if form.is_valid():
            client_object = Client.objects.filter(phone_number=form.cleaned_data['phone_number'])
            client_id = None
            if len( client_object ) == 0:
                client = Client()
                client.name = form.cleaned_data['name']
                client.phone_number = str(form.cleaned_data['phone_number'])
                client.save()
                client_id = client
            else:
                client_id = client_object[0]

            cart = Cart(request)
            order = Order()
            order.client_id = client_id
            order.dateTimeOrder = datetime.datetime.now()
            order.price = str(cart.get_total_price());

            order.city = form.cleaned_data['city']
            order.street = form.cleaned_data['street']
            order.house = str(form.cleaned_data['house'])
            order.entrance = str(form.cleaned_data['entrance'])
            order.apartament_number = str(form.cleaned_data['apartament_number'])
            order.save()

            for cart_item in cart.cart:
                product_order = Product_order()
                product_order.product_id = get_object_or_404(Product, id = int(cart_item) )
                product_order.quantity = int ( cart.cart[cart_item]['quantity'] )
                product_order.order_id = order
                product_order.save()
            cart.clear()
            return main_page(request)
        else:
            form = checkout_form
        return HttpResponse('bad')




def auth(request):
    return render (request, 'auth_page.html', {
        'auth_form': Auth_form(),
        'auth': Auth(request)
    })


class Authorization():
    def login(request):
        phone_number = request.GET.get('phone_number')
        code = request.GET.get('code')
        auth = Auth(request)
        auth.login(phone_number, code)
        return JsonResponse({
            "result": "1",
        })

    def logout(request):
        auth = Auth(request)
        auth.logout()
        return JsonResponse({
            "result": "1",
        })

    def personal_account(request):
        auth = Auth(request)
        if auth.is_authorization():
            client_object = auth.get_client_object()
            return render (request, 'personal_account.html', {
                "auth": auth,
                "client": client_object,
                'client_form': Client_form(initial = {
                    'phone_number': client_object.phone_number,
                    'name': client_object.name,
                    'email': client_object.email
                    }),
                'auth': Auth(request)
            })
        else:
            return HttpResponse("error")
    def get_code(request):
        auth = Auth(request)
        phone_number = request.GET.get('phone_number')
        auth.set_code(phone_number)
        return JsonResponse({
            "result": "1",
        })

    def change_client(request):
        auth = Auth(request)
        if auth.is_authorization():
            client_object = auth.get_client_object()
            client_object.name = request.POST.get("name")
            client_object.email = request.POST.get('email')
            client_object.save()
        return HttpResponse("success")



class ProductView():
    def addComment(request, product, client):
        text_comment = request.GET.get('text')
        new_comment = Product_comment()
        try:
            product_object = get_object_or_404(Product, id = product)
            client_object = get_object_or_404(Client, id = client)
        except:
            return

        new_comment.text = text_comment
        new_comment.product = product_object
        new_comment.client = client_object
        new_comment.save()

    def addRating(request):
        auth = Auth(request)
        if auth.is_authorization():
            client_object = auth.get_client_object();
            rating = request.GET.get('rating')
            product_id = request.GET.get('product_id')
            try:
                product_object = get_object_or_404(Product, id = product_id)
            except:
                product_object = Product()
            try:
                rating_object = get_object_or_404(Product_rating, client = client_object, product = product_object)
            except:
                rating_object = Product_rating()
            rating_object.client = client_object
            rating_object.product = product_object
            rating_object.rating = rating
            rating_object.save()
        return JsonResponse({
            "result": 1
        })

class DeliveryCost():
    def __get_object_delivery():
        pass

    def get_delivery_cost(request):
        cart = Cart(request)
        total_price = cart.get_total_price()
        delivery_cost = 150

        if total_price < 150:
            delivery_cost = 150 - total_price
            return delivery_cost
        else:
            return 0

    def get_delivery_cost(request):
        cart = Cart(request)
        total_price = cart.get_total_price()
        delivery_cost = 150

        if total_price < 150:
            delivery_cost = 150 - total_price
            return JsonResponse({
                "cost": delivery_cost,
                "total_price": 150
                })
        else:
            return JsonResponse({
                "cost": 0,
                "total_price": total_price
            })


    def get_pickup_cost(request):
        cart = Cart(request)

        total_price = cart.get_total_price()
        pickup_cost = float(total_price) * -0.2


        return JsonResponse({
            "cost": pickup_cost,
            "total_price": float(total_price) + pickup_cost
        })

    def get_delivery(request):
        cart = Cart(request)
        total_price = cart.get_total_price()
        delivery_cost = 150

        if total_price < 150:
            delivery_cost = 150 - total_price
            return delivery_cost
        else:
            return 0


    def get_pickup(request):
        cart = Cart(request)

        total_price = cart.get_total_price()
        pickup_cost = float(total_price) * -0.2


        return pickup_cost


class OtherView():
    def about_us(request):
        return render(request, "about_us.html", {
                'auth': Auth(request)
        })

    def contacts(request):
        return render(request, "contacts.html", {
                'auth': Auth(request)
        })
    def express(request):
        return render(request, "express.html", {
                'auth': Auth(request)
        })
    def error_page(request):
        return render(request, "error_page.html", {
                'auth': Auth(request)
        })
