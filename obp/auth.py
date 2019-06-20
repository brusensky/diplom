from django.conf import settings

from .models import Client_Auth, Client
from django.shortcuts import get_object_or_404
import random
import datetime
from obp.smsc_api import *

class Auth(object):
    def __init__(self, request):
        self.session = request.session
        self.session.set_expiry(0)
        #request.session.set_expiry(0)
        user = self.session.get(settings.USER_CLIENT_SESSION_ID)
        if not user:
            #Сохранение клиента в сессию
            user = self.session[settings.USER_CLIENT_SESSION_ID] = {
                'phone_number': None,
                'code_of_auth': None,
                'good': None,
            }
        self.user = user

    def save(self):
        self.session[settings.USER_CLIENT_SESSION_ID] = self.user
        # Указываем, что сессия изменена
        self.session.modified = True

    def send_sms(self, phone_number, code):
        text = 'vash kod dlya vhoda v lichnyj kabinet - ' + str(code)
        smsc = SMSC()

    def set_session(self, phone_number, code_of_auth):
        phone_number = phone_number
        code_of_auth = code_of_auth
        self.user = {
            'phone_number': phone_number,
            'code_of_auth': code_of_auth,
            'good': True
        }
        self.save()

    def is_authorization(self):
        try:
            obj = get_object_or_404(Client_Auth, phone_number = self.user["phone_number"] )
            if self.user['good'] == True and self.user["code_of_auth"] == obj.code_of_auth:
                return True
            else:
                return False
        except:
            return False

    def try_get_object(self):
        try:
            get_object_or_404(Client_Auth, phone_number = phone_number)
        except:
            obj = Client_Auth()
            obj.phone_number = phone_number
            obj.save()
        return obj

    def generateCode(self):
        code = random.randint(1000, 9999)
        print(code)
        return code


    def run(phone_number):
        obj = try_get_object(phone_number)
        code = generate_code()
        send_message(phone_number, code)

    def set_code(self, phone_number):
        try:
            obj = get_object_or_404(Client_Auth, phone_number = phone_number )
        except:
            obj = Client_Auth()
        obj.phone_number = phone_number
        obj.code_of_auth = self.generateCode()
        obj.end_of_live = datetime.now()# + datetime.timedelta(minutes=10)
        # self.send_sms(phone_number, obj.code_of_auth)
        obj.save()


    def get_client_object(self):
        try:
            print("fefewefwefwefwefwef")
            client_object = get_object_or_404(Client, phone_number = self.user["phone_number"])
            return client_object
        except:
            return
    def get_client_id(self):
        try:
            client_object = get_object_or_404(Client, phone_number = self.user["phone_number"])
            return client_object.id
        except:
            return False



    def login(self, phone_number, code_of_auth):
        try:
            obj = get_object_or_404(Client_Auth, phone_number = phone_number)
            if obj.phone_number == phone_number and obj.code_of_auth == code_of_auth:
                self.set_session(phone_number, code_of_auth)
        except:
            return False
    def logout(self):
        del self.session[settings.USER_CLIENT_SESSION_ID]
        self.session.modified = True
