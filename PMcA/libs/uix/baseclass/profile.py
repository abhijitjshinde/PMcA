from main_imports import (MDDialog, MDFlatButton, MDGridBottomSheet, MDScreen,
                          OneLineTextDialog)

from libs.applibs import utils
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.storage.jsonstore import JsonStore
import requests
from kivy.network.urlrequest import UrlRequest
import json
import os
utils.load_kv("profile.kv")

class Profile_Screen(MDScreen):
    key1 =''
    def on_pre_enter(self, *args):
        # self.select_path('/')
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
        )
        file_path = 'profile.json'
        userinfo = 'UserInfo.json'
        try:
            if os.path.getsize(file_path) != 0:
                with open(file_path) as f:
                    data = json.load(f)
                    print(data)
                    value = data
                    self.ids.profile_image.background_normal = value
                    self.ids.profile_image.background_down = value
            else:
                # try:
                Internet_check = requests.get('https://pmca-a03a7-default-rtdb.firebaseio.com/.json')
                if Internet_check.ok == True:
                    url ="https://pmca-a03a7-default-rtdb.firebaseio.com/9594897959/details/.json"
                    request  = requests.get(url)            
                    data = request.json()
                    path = data["Profile_pic"]
                    self.Update_profile_image(path)
                else:
                    print("I Am OFFLINE Keep ME Online")
                # except requests.exceptions.RequestException as e:  # This is the correct syntax
                #     print("You are Offline")
            if os.path.getsize(userinfo) != 0:
                with open(userinfo) as f:
                    data = json.load(f)
                    key, value = list(data.items())[0]
                    self.key1 = key
                    P_Name = data[key]['Name']
                    P_Username = data[key]['Username']
                    self.ids.profile_name.secondary_text = P_Name
                    self.ids.profile_username.secondary_text ='@'+ P_Username
                    self.ids.profile_Phone.secondary_text =key
        except FileNotFoundError:
            print("file not Found")
# file Manager section---------------------------------
    def file_manager_open(self):
        print('hello.......')
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''        
        data = path
        self.Update_profile_image(path)
        self.exit_manager()
        JsonStore("profile.json")
        try:
            with open('profile.json','w') as f:
                json.dump(data,f)
                print("UserInfo file is modified...")

        except KeyError:
            print("the data is not stored...")
        toast(path)
    def Update_profile_image(self,path):
        '''This will update image in DataBase and profile section in App Also'''
        # https://pmca-a03a7-default-rtdb.firebaseio.com/9594897959/details/Profile_pic
        url1 = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.key1+"/details/.json"            
        file = {
                "Profile_pic" : path
                }
        try:
            requests.patch(url1,json = file)
            self.ids.profile_image.background_normal = path
            self.ids.profile_image.background_down = path
        except requests.exceptions.RequestException as e:
            print("no internet ")
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
    # file manager ends ----------------------------------------------------- 
    
    def change_profile_data(self,widget):
        """Change text data using Dialog box.
        [widget] change this widget text"""
        dialogObj =None
        Dialog=OneLineTextDialog()
        def cancel_btn(btn):
            # use function when CANCEL btn click
            dialogObj.dismiss(force=True)
        def ok_btn(btn):
            # use function when OK btn click
            changed_name = Dialog.ids.dialog_text.text
            widget.secondary_text = changed_name
            url1 = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.key1+"/details/.json"            
            file = {
                    "Name" : changed_name
                    }
            requests.patch(url1,json = file)
            request  = requests.get(url1)            
            data = request.json()
            userinfo = {self.key1:data}
            try:
                with open('UserInfo.json','w') as f:
                    json.dump(userinfo,f)
                    print("UserInfo file is modified...")
            except KeyError:
                print("the data is not stored...")
            cancel_btn(btn)
        
        if not dialogObj:
            dialogObj=MDDialog(
                auto_dismiss=True,
                title= widget.secondary_text,
                type="custom",
                content_cls=Dialog,
                buttons=[
                    MDFlatButton(
                        text="CANCEL", 
                        # text_color=self.theme_cls.primary_color,
                        on_release=cancel_btn,
                    ),
                    MDFlatButton(
                        text="OK", 
                        # text_color=self.theme_cls.primary_color,
                        on_release=ok_btn,
                    ),
                ],
            )
        dialogObj.open()
        
    
    def change_profile_img(self):
        """
        method call when image click on profile_view page.
        if it's user own profile than show options of change.
        """
        bottom_sheet_menu = MDGridBottomSheet(
            animation=True,
        )
        data = {
            "Upload": "cloud-upload",
            "Camera": "camera",
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.file_manager_open(),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()
    
    def Logout(self):
        f = open("UserInfo.json", "r+")  
        m = open("profile.json", "r+")  
        n = open("ChatHub.json", "r+")  
        # p = open("database.json", "r+")  
        # absolute file positioning 
        f.seek(0)  
        m.seek(0)  
        n.seek(0)  
        # to erase all data  
        f.truncate()
        m.truncate()
        n.truncate()
        self.ids.profile_image.background_normal = "assets//img//blank_profile.png"
        self.ids.profile_image.background_down = "assets//img//blank_profile.png"
        self.parent.change_screen("login") 