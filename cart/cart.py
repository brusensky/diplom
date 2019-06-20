from decimal import Decimal
from django.conf import settings
from obp.models import Product
from django.shortcuts import get_object_or_404

class Cart(object):
    #Инициализация
    def __init__(self,request):
        #Инициализация корзины пользователя

        self.session = request.session
        self.session.set_expiry(0)
        #request.session.set_expiry(0)
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #Сохранение корзины в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    # Добавление товара в корзину пользователя
    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1,
                                     'price': str( product.get_price() ),
                                     }
        self.save()

    #Повышение количества товара в корзине на 1
    def plus_quantity(self, product):
        product_id = str(product.id)
        self.cart[product_id]['quantity'] += 1
        self.save()

    #Понижение количества товара в корзине на 1
    def minus_quantity(self, product):
        product_id = str(product.id)
        if (self.cart[product_id]['quantity'] > 1):
            self.cart[product_id]['quantity'] -= 1
        else:
            self.remove(product)
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    # Итерация по товарам
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # Количество товаров
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def getCartList(self):
        cartList = []
        flag = False
        for product in self.cart:
            obj = get_object_or_404(Product, id = product)
            cartList.append({
            "id": product,
            "img_url": obj.image.url,
            "title": obj.title,
            "quantity": self.cart[product]['quantity'],
            "price": self.cart[product]['price'],
            "total_price": self.cart[product]['quantity'] * float(self.cart[product]['price'])
            })
            flag = True
        if flag:
            return cartList
        return False

    def getCartListId(self):
        cartList = []
        for product in self.cart:
            obj = get_object_or_404(Product, id = product)
            cartList.append(obj.id)
        return cartList
