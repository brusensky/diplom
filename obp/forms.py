from django.forms import ModelForm
from django import forms

from .models import *
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

class checkout_form_order(ModelForm):
    class Meta:
        model = Order
        fields  = ['city', 'street', 'house', 'entrance', 'apartament_number']
    def __init__(self, *args, **kwargs):
        super(checkout_form_order, self).__init__(*args, **kwargs)
        self.fields['city'].widget.attrs['placeholder'] = "Город"
        self.fields['street'].widget.attrs['placeholder'] = "Улица"
        self.fields['house'].widget.attrs['placeholder'] = "Дом"
        self.fields['entrance'].widget.attrs['placeholder'] = "Этаж"
        self.fields['apartament_number'].widget.attrs['placeholder'] = "Квартира"


class checkout_form_client(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'email']

    def __init__(self, *args, **kwargs):
        super(checkout_form_client, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs['placeholder'] = "Номер телефона"
        self.fields['name'].widget.attrs['placeholder'] = "Имя"
        self.fields['email'].widget.attrs['placeholder'] = "@mail"

        # self.fields['phone_number'].widget.attrs.update({
        #     'class': 'form-control',
        #     'id': 'inlineFormInputGroup'
        # })





class Client_form(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'email']
    def __init__(self, *args, **kwargs):
        super(Client_form, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs['readonly'] = True
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inlineFormInputGroup'
        })
        #self.fields['email'].widget.attrs['id'] = 'inlineFormInputGroup';


class Comment_form(ModelForm):
    class Meta:
        model = Product_comment
        fields = ['text']
    def __init__(self, *args, **kwargs):
        super(Comment_form, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = "Текст вашего комментария..."



class Auth_form(forms.Form):
    #phone_number = PhoneNumberField()

    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField()#(validators=[phone_regex], max_length=17) # validators should be a list
    code = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(Auth_form, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs.update({'class': 'phone_number'})
        self.fields['phone_number'].widget.attrs['placeholder'] = "Номер телефона"
        self.fields['code'].widget.attrs.update({'class': 'code'})
        self.fields['code'].widget.attrs['placeholder'] = "Код"
