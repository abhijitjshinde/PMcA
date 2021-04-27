from main_imports import ImageLeftWidget, MDScreen, TwoLineAvatarListItem
from libs.applibs import utils
# Python imports
import sys
import requests
import json
import os
utils.load_kv("home.kv")

class Home_Screen(MDScreen):
    loginId = ''
    internet = 1
    url = 'https://pmca-a03a7-default-rtdb.firebaseio.com/'
    chat_file = 'ChatHub.json'
    file_path = 'UserInfo.json'
    database = 'database.json'
    username = set()
    def on_pre_enter(self, *args):
        try:
            if os.path.getsize(self.file_path) != 0:
                with open(self.file_path) as f:
                    data = json.load(f)
                    key, value = list(data.items())[0]
                    self.loginId = key
                url1 = self.url+self.loginId+'/chats.json'
                print("i am from home page",self.loginId," url: ",url1)
                try:
                    all_chats = requests.get(url1)
                    chats_data = all_chats.json()
                
                # To store All Chats in local json file(ChatHub.json)
                    with open('ChatHub.json','w') as C:
                        json.dump(chats_data,C) 
                    
                # This is for looking which chat numbers present
                    # for i in chats_data : 
                    #     print("chats numbers",i)
                except requests.exceptions.RequestException:  # This is the correct syntax
                    # Offline code goes here.. Load the ChatHub.json file to Screen
                    print("You are Offline")
                    self.parent.Bottom_msg("Please Turn On Internet..")
                    # twolineW= TwoLineAvatarListItem(text=f"Hamster",
                    #     secondary_text="@username",
                    #     on_touch_up=self.chat_room)

                    # twolineW.add_widget(ImageLeftWidget(source="assets//img//hamster_icon.png"))
            
                    # self.screen_manager.get_screen("home").ids.chat_tab.add_widget(twolineW)
            else:
                print("file is empty")
        except FileNotFoundError:
            print("file not Found")        
    def on_enter(self, *args):
        try:
            request = requests.get("https://www.google.com/")
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print("You are Offline")
            self.parent.Bottom_msg("Please Turn On Internet..")
            self.internet = 0
        chat_number_data = set()
        if self.internet == 1:
            with open(self.file_path) as f:
                data = json.load(f)
                key, value = list(data.items())[0]
            print("This is url from Home/on enter---> ",self.url+key+'/chats/.json')
            all_chat_data = requests.get(self.url+key+'/chats/.json')
            if all_chat_data.json() != "None":
                with open(self.database) as g:
                    data_1 = json.load(g)
                for i in all_chat_data.json():                    
                    chat_number_data.add(i)
                    if data_1[i] not in self.username:
                        self.username.add(data_1[i])
                        self.all_chats(data_1[i])
            else:
                print("No data available")
        else:
            with open(self.database) as g:
                data_1 = json.load(g)
            with open(self.chat_file) as d:
                chats = json.load(d)
            for i in chats:
                chat_number_data.add(i)
                if data_1[i] not in self.username:
                    self.username.add(data_1[i])
                    self.all_chats(data_1[i])

        print("this is on enter section of home : ",chat_number_data)
        print("this is on enter section of home list : ",self.username)
    def all_chats(self,name):
        """
        All Chat that show in home chat tab. all chat are added by 
        this method. it will use in differe t in future.
        """     
        # self.change_screen("profile")
        #Load All chat from file...add()  
        twolineW= TwoLineAvatarListItem(text= name,
            # secondary_text='i',
            on_press=self.chat_room)
        twolineW.add_widget(ImageLeftWidget(source="assets//img//pro.jpg"))        
        self.parent.get_screen("home").ids.chat_tab.add_widget(twolineW)

    def chat_room(self,touch):
        """Switch to Chatroom. but username and chatroom username 
        change according to which one you touch in chat list"""
        
        name = touch.text
        print("Screen Name",name)
        self.parent.get_screen("chat_room").ids.profile_bar.title = name
        # self.parent.get_screen("chat_room").use = name
        self.parent.change_screen("chat_room")
    def search_account(self,search_field):
        """
        this method use when search button pressed search_field
        contain data in string that you want to search on hamster server
        """
        database_path = 'database.json'
        try:
            if os.path.getsize(database_path) != 0:
                with open(database_path) as f:
                    data = json.load(f)                    
        except FileNotFoundError:
            print("file not Found")
        numbers = set()
        uasername = set()
        for key,value in data.items():
            numbers.add(key)
            uasername.add(value)
        # for dummy search item [------
        if search_field in uasername:
            twolineW= TwoLineAvatarListItem(text=f"{search_field}",
                secondary_text=f"@{search_field}",on_press=self.chat_room)

            twolineW.add_widget(ImageLeftWidget(source="assets//img//hamster_icon.png"))
            
            self.ids.search_items.add_widget(twolineW)
        # #  ----- ] end dummy search
    
    