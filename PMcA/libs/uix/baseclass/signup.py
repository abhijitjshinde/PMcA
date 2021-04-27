from main_imports import MDScreen
from libs.applibs import utils
from libs.uix.baseclass.login import Login_Screen
from kivy.properties import BooleanProperty, StringProperty
from libs.uix.baseclass.login import Login_Screen
from kivy.uix.screenmanager import ScreenManager

from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore


import sys
import requests
import json
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from json import dumps 
import os.path


from libs.uix.baseclass.login import Login_Screen

from libs.uix.baseclass.root import Root
# from libs.uix.baseclass.signup import Signup_Screen
# from libs.uix.baseclass.verification import Verification_Scree


utils.load_kv("signup.kv")

class Signup_Screen(MDScreen):
    debug = False
    url  = "https://pmca-a03a7-default-rtdb.firebaseio.com/.json"

    def Sign_me_up(self,Phone,Name,Username):       
        if Phone != '' and Name != '' and Username != '':
            # signup_info = str({f'\"{Phone}\":{{"Name":\"{Name}\","Username":\"{Username}\","profile_pic":" ","chats":" "}}'})
            # signup_info = str({f'\"{Phone}\": {{"details" : {"Name" : \"{Name}\","Profile_pic" : " ","Username" : \"{Username}\"},"chats" : " "}}'})
            signup_info =  str({f'\"{Phone}\":{{"details" : " ","chats" : "None"}}'})
            
            signup_info = signup_info.replace(".","-")
            signup_info = signup_info.replace("\'","")
            url  = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+Phone+"/details/.json"
            patch_req = {"Name" : Name,"Profile_pic" : " ","Username" : Username}
            to_database = json.loads(signup_info)
            # patch_up = json.loads(patch_req)
            # print((to_database))
            requests.patch(url = self.url,json = to_database)
            requests.patch(url = url,json = patch_req)
            self.parent.change_screen("login")
        else:
            print("Something Went Wrong...")
        
    