from django.db import models
from django.utils.html import format_html
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator, URLValidator
import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class Section(models.Model):
    id = models.AutoField(primary_key = True, verbose_name = "код")

    title = models.CharField(max_length = 25, verbose_name = "название", validators = [MinLengthValidator(2)])

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


#Модель товара
class Product(models.Model):
    GRAM = 'г.'
    LITER = 'л.'
    UNIT_SIZE  = (
        (GRAM, GRAM),
        (LITER, LITER)
    )
    id = models.AutoField(primary_key = True, verbose_name = "код товара");

    section_id = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name = "категория")

    title = models.CharField(
        max_length=25,
        verbose_name = "название товара",
        unique = True,
        validators = [MinLengthValidator(2)]
        )
    size = models.DecimalField(
        max_digits = 5,
        decimal_places = 1,
        verbose_name = "вес",
        validators=[MinValueValidator(1), MaxValueValidator(9999)]
        )
    unitSize = models.CharField(
        max_length = 3,
        choices = UNIT_SIZE,
        default = GRAM,
        verbose_name = "единица измерения веса"
        )
    price = models.PositiveSmallIntegerField(verbose_name = "цена", validators = [MaxValueValidator(9999), MinValueValidator(1)] )
    image = models.ImageField(upload_to="", blank=True, verbose_name = "изображение")
    date = models.DateField(default=datetime.date.today, verbose_name = "дата добавления")

    def __str__(self):
        return self.title
    def is_Stock(self):
        try:
            object = Stock.objects.get( product_id = self.id , status = True)
            return object
        except:
            return
    def get_price(self):
        try:
            object = Stock.objects.get( product_id = self.id , status = True)
            return object.value
        except:
            pass
        return self.price
    def getPrice(self):
        try:
            object = Stock.objects.get( product_id = self.id , status = True)
            return format_html('<del class = "price">{} грн.</del> <spanс class = "price">{} грн. </span>'.format(self.price, object.value) )
        except:
            pass
        #else:
        return format_html('<span class = "price">' + str( self.price ) + ' грн.</span>')
    def get_average_rating(self):
        try:
            rating_object = Product_rating.objects.filter( product = self.id )
            count = 0
            rating = 0
            for item in rating_object:
                count += 1
                rating += item.rating

            return {
                "rating": rating / count,
                "count": count
            }
        except:
            return {
                "rating": 0,
                "count": 0
            }

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


#модель
class Product_composition(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = "Код")

    ingradient = models.CharField(max_length = 40, verbose_name = "ингредиент")

    def __str__(self):
        return self.ingradient
    class Meta:
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"

#Таблица специальных предложений, которые отображаются на слайде на главной странице
class Special_offers(models.Model):
    title = models.CharField(max_length = 30, verbose_name = "Название")
    url = models.URLField(max_length = 300, verbose_name = "URL-адрес")
    image = models.ImageField(upload_to="", verbose_name = "Изображение")
    status = models.BooleanField(verbose_name = "Статус")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Специальное предложение"
        verbose_name_plural = "Специальные предложения"

class Stock(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = "товар" )

    value = models.PositiveSmallIntegerField(verbose_name = "цена со скидкой")
    status = models.BooleanField(verbose_name = "статус")

    def __str__(self):
        #return 'Акция №' + str( self.id )
        return self.product_id.title
    class Meta:
        verbose_name = "акция"
        verbose_name_plural = "акции"

class Client(models.Model):
    id = models.AutoField(primary_key = True, verbose_name = "код")

    name = models.CharField(max_length = 50, verbose_name = "имя")
    phone_number = models.CharField(verbose_name = "номер телефона", max_length = 15)
    email = models.EmailField(max_length = 100, verbose_name = "Электронная почта", null = True, blank = True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

class Client_Auth(models.Model):

    phone_number = models.CharField(max_length = 15)
    code_of_auth = models.CharField(max_length = 6)
    end_of_live = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(minutes=10) )
    class Meta:
        verbose_name = "Код для авторизации клиента"
        verbose_name_plural = "Коды для авторизации клиентов"

#Заказ
class Order(models.Model):
    STATUS_EXPACTION = "Ожидание подтверждения"
    STATUS_TREATMENT = "В обработке"
    STATUS_WAIT_PICK_UP = "Ожидается самовывоз"
    STATUS_WAIT_DELIVERY = "Ожидается отправки"
    STATUS_DELIVERY = "В пути"
    STATUS_SUCCESS = "Заказ получен"
    STATUS_CANCEL = "Заказ отклонен"
    STATUS_CHOICES = (
        (STATUS_EXPACTION, STATUS_EXPACTION),
        (STATUS_TREATMENT, STATUS_TREATMENT),
        (STATUS_WAIT_PICK_UP, STATUS_WAIT_PICK_UP),
        (STATUS_WAIT_DELIVERY, STATUS_WAIT_DELIVERY),
        (STATUS_DELIVERY, STATUS_DELIVERY),
        (STATUS_SUCCESS, STATUS_SUCCESS),
        (STATUS_CANCEL, STATUS_CANCEL),
    )

    id = models.AutoField(primary_key = True, verbose_name = "код")

    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name = "клиент")
    #delivery = models.ForeignKey(DeliveryCost, on_delete=models.CASCADE, verbose_name = "доставка")
    #delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, default = 1)
    #adress_id = models.ForeignKey(Adress, on_delete=models.CASCADE)
    #delivery_id = models.ForeignKey(Delivery, on_delete=models.CASCADE)

    dateTimeOrder = models.DateTimeField(verbose_name = "дата и время заказа")
    price = models.PositiveIntegerField(verbose_name = "сумма заказа")
    deliveryCost = models.DecimalField(verbose_name = "сумма доставки", default = "0", max_digits = 4, decimal_places = 1)
    #Адрес
    city = models.CharField(max_length = 25, verbose_name = "город", null = True)
    street = models.CharField(max_length = 25, verbose_name = "улица", null = True)
    house = models.PositiveIntegerField(verbose_name = "номер дома", null = True)
    entrance = models.PositiveSmallIntegerField(verbose_name = "этаж", null = True)
    apartament_number = models.PositiveIntegerField(verbose_name = "квартира", null = True)

    status = models.CharField( max_length = 30, choices = STATUS_CHOICES, default = STATUS_EXPACTION, verbose_name = "статус")

    def __str__(self):
        return str(self.id)

    def get_html_status(self):
        if self.status == self.STATUS_EXPACTION:
            return format_html('<span style = "color: orange; font-weight: bold;">'+self.status+'<span>')
        if self.status == self.STATUS_TREATMENT:
            return format_html('<span style = "color: yellow; font-weight: bold;">'+self.status+'<span>')
        if self.status == self.STATUS_WAIT_PICK_UP:
            return format_html('<span style = "color: darkblue; font-weight: bold;">'+self.status+'<span>')
        if self.status == self.STATUS_WAIT_DELIVERY:
            return format_html('<span style = "color: darkblue; font-weight: bold;">'+self.status+'<span>')
        if self.status == self.STATUS_DELIVERY:
            return format_html('<span style = "color: blue; font-weight: bold;">'+self.status+'<span>')
        if self.status == self.STATUS_SUCCESS:
            return format_html('<span style = "color: lightgreen; font-weight: bold;">'+self.status+'<span>')
        if self.status == self.STATUS_CANCEL:
            return format_html('<span style = "color: red; font-weight: bold;">'+self.status+'<span>')

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"


class Product_order(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name = "номер заказа")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = "наименование товара")

    quantity = models.PositiveSmallIntegerField(verbose_name = "количество")

    def __str__(self):
        return str(self.product_id)
    class Meta:
        verbose_name = "товар в заказ"
        verbose_name_plural = "товары в заказе"


class Product_comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    text = models.TextField(max_length = 500)
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

class Product_rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    class Meta:
        verbose_name = "Рейтинг товара"
        verbose_name_plural = "Рейтинг товаров"
