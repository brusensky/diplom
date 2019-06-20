from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from obp.models import  *
from django.utils.html import format_html
from jet.admin import CompactInline
#from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
# Register your models here.

#admin.site.register(Special_offers)
#admin.site.register(Stock)
#admin.site.register(Product_order)
class ProductCompositionInline(admin.TabularInline):
    model = Product_composition

class OrderInline(admin.TabularInline):
    model = Product_order

class Client_OrderInline(admin.TabularInline):
    model = Order

class MyAdminSite(AdminSite):
    site_header = 'Pizza-Day'
    index_template = "admin/index.html"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    #Создание ценового фильтра
    class PriceListFilter(admin.SimpleListFilter):
        title = 'Цена'
        parameter_name = 'цена'
        #Название фильтров
        def lookups(self, request, model_admin):
            return (
                ('1', 'до 199'),
                ('2', '200 - 299'),
                ('3', '300 - 449'),
                ('4', 'от 450'),
            )
        #Запрос на выборку
        def queryset(self, request, queryset):
            if self.value() == '1':
                return queryset.filter(price__gte= 0,
                                        price__lte=199)
            if self.value() == '2':
                return queryset.filter(price__gte = 200,
                                        price__lte = 299)
                return go()
            if self.value() == '3':
                return queryset.filter(price__gte = 300,
                                        price__lte = 449)
            if self.value() == '4':
                return queryset.filter(price__gte=200,
                                        price__lte=299)
    #Отображаемые поля
    list_display = ('get_image_html', 'id', 'section_id', 'title', 'getSize', 'getPrice'  )

    list_displat_links = ('')

    inlines = [
        ProductCompositionInline
    ]
    #Поле по которому можно сделать поиск
    search_fields = ['title']
    #Список фильтраций
    list_filter = ['section_id', PriceListFilter]

    #Получение html блока с рисунком товара
    def get_image_html(self, obj):
        return format_html('<img src = "{}" style = "height: 30px; border-radius: 5px;"></img>', obj.image.url)
    get_image_html.short_description = "Фото товара"

    #Получение цены
    def getPrice(self, obj):

        try:
            object = Stock.objects.get( id = obj.id , status = True)
            return format_html("<del>{} грн.</del> <span>{} грн. </span>".format(obj.price, object.value) )
        except:
            pass
        #else:
        return format_html("<span>" + str( obj.price ) + " грн." + "</span>")
    getPrice.short_description = "Цена"

    #Получение строки веса + его еденицу измерения
    def getSize(self, obj):
        return str( obj.size ) + obj.unitSize
    getSize.short_description = "Вес"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    class PriceListFilter(admin.SimpleListFilter):
        title = 'Цена'
        parameter_name = 'цена'
        def lookups(self, request, model_admin):
            return (
                ('1', 'до 199'),
                ('2', '200 - 299'),
                ('3', '300 - 449'),
                ('4', 'от 450'),
            )

        def queryset(self, request, queryset):
            if self.value() == '1':
                return queryset.filter(price__gte= 0,
                                        price__lte=199)
            if self.value() == '2':
                return queryset.filter(price__gte = 200,
                                        price__lte = 299)
            if self.value() == '3':
                return queryset.filter(price__gte = 300,
                                        price__lte = 449)
            if self.value() == '4':
                return queryset.filter(price__gte=200,
                                        price__lte=299)

    list_display = ('id', 'dateTimeOrder', 'price', 'status' )
    list_filter = ['dateTimeOrder', PriceListFilter, "status"]
    list_editable = ["status"]

    inlines = [
        OrderInline
    ]

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number' )
    inlines = [
        Client_OrderInline
    ]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class StockAdmin(admin.ModelAdmin):
    list_display = ("product_id", "value", "status" )
    search_fields = ['product_id__title']
    list_filter = ['status']

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Product, ProductAdmin)
admin_site.register(Client, ClientAdmin)
admin_site.register(Order, OrderAdmin)
admin_site.register(Section, SectionAdmin)
admin_site.register(Stock, StockAdmin)
admin_site.register(Product_comment)
admin_site.register(Client_Auth)
admin_site.register(Special_offers)
admin_site.register(Product_rating)



# 
#
# class CustomIndexDashboard(Dashboard):
#     columns = 3
#
#     def init_with_context(self, context):
#         self.available_children.append(modules.LinkList)
#         self.children.append(modules.LinkList(
#             _('Support'),
#             children=[
#                 {
#                     'title': _('Django documentation'),
#                     'url': 'http://docs.djangoproject.com/',
#                     'external': True,
#                 },
#                 {
#                     'title': _('Django "django-users" mailing list'),
#                     'url': 'http://groups.google.com/group/django-users',
#                     'external': True,
#                 },
#                 {
#                     'title': _('Django irc channel'),
#                     'url': 'irc://irc.freenode.net/django',
#                     'external': True,
#                 },
#             ],
#             column=0,
#             order=0
#         ))
