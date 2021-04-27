#--[Start platform specific code]
"""This code to detect it's Android or not 
if it's not android than app window size change in android phone size"""
from kivy.utils import platform

if platform != 'android':
    from kivy.config import Config
    Config.set("graphics","width",360 )
    Config.set("graphics","height",640)
#--[End platform specific code]

#--[Start Soft_Keyboard code ]
"""code for android keyboard. when in android keyboard show textbox 
automatic go to top of keyboard so user can see when he type msg"""
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore

Window.keyboard_anim_args = {"d":.2,"t":"linear"}
Window.softinput_mode = "below_target"
#--[End Soft_Keyboard code ]
 
from libs.uix.baseclass.chat_room import Chat_Room_Screen 
from libs.uix.baseclass.forgot import Forgot_Screen
from libs.uix.baseclass.home import Home_Screen
from libs.uix.baseclass.login import Login_Screen
from libs.uix.baseclass.profile import Profile_Screen
from libs.uix.baseclass.root import Root
from libs.uix.baseclass.signup import Signup_Screen
from libs.uix.baseclass.verification import Verification_Screen
from main_imports import ImageLeftWidget, MDApp, TwoLineAvatarListItem
# from kivy.storage.jsonstore import JsonStore

# Other Imports
import json
import jsonpatch
import os
import requests


class PMcA(MDApp):
    """
    Hamster App start from here this class is root of app.
    in kivy (.kv) file when use app.method_name app is start from here
    """
    internet = 1
    def __init__(self, **kwargs):
        super(PMcA, self).__init__(**kwargs)
        # Global Variables
        self.APP_NAME = "PMcA"
        self.COMPANY_NAME = "PMcA.org"
        self.theme_cls.primary_palette = "DeepPurple"
        #check if internet is available  or not
        # Chat Search Data
        JsonStore("database.json")
        self.path = "Info.json"
        src = "database.json"  
        try:
            fetch_data = requests.get('https://pmca-a03a7-default-rtdb.firebaseio.com/.json')
            if fetch_data.ok == True:
                data = fetch_data.json()
                my_list = {}
                for key,value in data.items():            
                    my_list[key] = data[key]['details']['Username']
                    print("User_Name : ",key,"---->",data[key]['details']['Username'])
                    # print("data appended in list")        
                    try:
                        with open(src,'w') as f:
                            json.dump(my_list,f)
                            print("database file is modified...")
                    except KeyError:
                        print("the data is not stored...")
            else:
                self.internet = 0
                Root.Bottom_msg("INTERNET is Not Available...")
                print("INTERNET is Not Available...")
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("You are Offline")
            self.internet = 0
            
            

        # except requests.exceptions.HTTPError as err:
        #     print("You are Offline Enjoy")            
        # except requests.NewConnectionError as m:
        #     print("You are Offline..")
        # except requests.HTTPSConnectionPool:
            # print("You are Offline now") 
        except KeyError:
            print("You are Offline now")   

    def build(self):
        """
        This method call before on_start() method so anything
        that need before start application all other method and code 
        write here.
        """
        # self.theme_cls.primary_palette = "Blue"
        # self.theme_cls.primary_hue = "500"

        # self.theme_cls.accent_palette = "Amber"
        # self.theme_cls.accent_hue = "500"

        # self.theme_cls.theme_style = "Light"
    
        self.screen_manager = Root()
        self.screen_manager.add_widget(Login_Screen())
        self.screen_manager.add_widget(Signup_Screen())
        self.screen_manager.add_widget(Forgot_Screen())
        self.screen_manager.add_widget(Verification_Screen())
        self.screen_manager.add_widget(Home_Screen())
        self.screen_manager.add_widget(Chat_Room_Screen())
        self.screen_manager.add_widget(Profile_Screen())        

        return self.screen_manager
    
    def on_start(self):
        """
        Anything we want to run when start application that code is here.
        """
        # JsonStore("Homepage.json")
        self.screen_manager.change_screen("login")
        file_path = 'UserInfo.json'       
        if os.path.getsize(file_path) != 0:
            self.screen_manager.change_screen("home")
            with open(file_path) as f:
                data = json.load(f)
                key, value = list(data.items())[0]
            if self.internet == 1:
                file = requests.get('https://pmca-a03a7-default-rtdb.firebaseio.com/'+key+'/chats.json')
                data = file.json()
                print('https://pmca-a03a7-default-rtdb.firebaseio.com/'+key+'/chats.json')
                print("--------From main.py to dump chats -----",data,"---------ends-------------")
                try:
                    with open('ChatHub.json','w') as C:
                        json.dump(data,C)
                except FileExistsError:
                    print("file is exist ")
            else:
                # Root().Bottom_msg("Please Turn On Internet..")
                pass            
        else:
            self.screen_manager.change_screen("login")

            

if __name__ == "__main__":
    # Start application from here.
    PMcA().run() 