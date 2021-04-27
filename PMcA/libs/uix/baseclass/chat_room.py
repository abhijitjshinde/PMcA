from main_imports import MDCard, MDLabel, MDScreen, MDSeparator, MDGridBottomSheet, UrlRequest
from libs.applibs import utils
from kivymd.uix.chip import MDChip
from kivymd.uix.filemanager import MDFileManager
import json
import os
import requests
import datetime
utils.load_kv("chat_room.kv")

class Chat_Room_Screen(MDScreen):
    chat_room_no = ''
    owner_no = ''
    url = ""
    check_set = set()
    def on_enter(self, *args):
        self.owner_no = self.parent.get_screen("home").loginId
        with open('ChatHub.json','r') as f:
            chats = json.load(f)
        with open('database.json','r') as f:
            numbers_show = json.load(f)
        if os.path.getsize('ChatHub.json') != 0:
            self.use = self.ids.profile_bar.title
            self.chat_room_no = self.get_key(self.use)
            if self.chat_room_no not in chats.keys():
                print("no dont have")
                # self.search_chat_room(self.chat_room_no)
            else:
                if self.chat_room_no != str :
                    chat_data = chats[self.chat_room_no]         
                else:
                    numb=self.get_key(self.chat_room_no)
                    chat_data = chats[numb]
            
            # print("This is dATA ---->:",chat_data)
            # print("U CAN SEE THE CHAT NUMBER ----------->",self.chat_room_no)
                for key,value in chat_data.items():                        
                    print("This is date",key)
                    # for i in key:                    
                    v = value
                    vl = v[-1]
                    # for i in value:
                    #     v = value[i]
                    #     vl = v[-1]
                    if vl == "1":
                        self.rx_msg(v,key)
                    else:
                        self.send_msg(v,key)
                    print("This is time",key)
                    print("This is msg",v)
                self.up_set()
        else: 
            print("no Chat data Available")
    def up_set(self):
        self.url = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats/"+self.chat_room_no+"/.json"            
        self.url_date = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats/"+self.chat_room_no+"/"+str(datetime.date.today())+".json"            
        self.check = UrlRequest(url=self.url,on_success=self.res,on_progress=print("url : ",self.url ))            
    def get_key(self,use):
        with open('database.json','r') as f:
            data = json.load(f)
        for key, value in data.items():
            if use == value:
                return key
        return "key does not exist"
    def chat_textbox(self):
        """
            MDCard size change when MSGbox use multilines.
            MDCard y axis size incress when MSGbox y axis size incress
        """
        fixed_Y_size = self.ids.root_chatroom.size[1]/3
        msg_textbox=self.ids.msg_textbox.size
        
        if msg_textbox[1] <= fixed_Y_size:
            
            self.ids.send_card.size[1]=msg_textbox[1]
            print(msg_textbox)
        else:
            self.ids.send_card.size[1]=fixed_Y_size
    
    def send_msg(self,msg_data,i):
        """
            When send button use to send msg this function call
            and clear MSGbox 
        """        
        if msg_data[-1] == '0' or msg_data[-1] == '1':
            msg_data = msg_data
        else:
            msg_data = msg_data + '0'
        print(" i am in send msg",msg_data[-1])

        msg_data = msg_data[0:len(msg_data)-1] # this is Msg
        text_msg = MDLabel(text=i,theme_text_color="Hint",font_style="Overline",text_size=(self.width, None),halign= "right")        
        sizeX = self.ids.root_chatroom.size[0]-20
        sizeY = self.ids.msg_textbox.size[1]
        # ->> sizeY is equal to msg_textbox sizeY because text_msg sizeY not work 
        # that's why i use msg_textbox is called 'Jugaad'
        msg_card= MDCard(
            size_hint=[None,None],
            size=[sizeX,sizeY],
            padding=20,
            elevation=9,
            ripple_behavior= True,
            radius= [25,25,0,25 ],            
    
        )
        
        msg_card.add_widget(MDLabel(
            text= msg_data,
            theme_text_color= "Primary",
            size_hint_y= None,
            height= 30
        ))        
        msg_card.md_bg_color = [236/255.0,156/255.0,247/255.0,1]
        self.ids.all_msgs.add_widget(msg_card)
        self.ids.all_msgs.add_widget(text_msg)
        self.ids.msg_scroll_view.scroll_to(msg_card)
        self.ids.msg_textbox.text=""
    def send_msg_btn(self,msg_data,i):
        if i == '':
            now = datetime.datetime.now()
            i = now.strftime("%H:%M:%S")
        text_msg = MDLabel(text=i,theme_text_color="Hint",font_style="Overline",text_size=(self.width, None),halign= "right")        
        sizeX = self.ids.root_chatroom.size[0]-20
        sizeY = self.ids.msg_textbox.size[1]
        # ->> sizeY is equal to msg_textbox sizeY because text_msg sizeY not work 
        # that's why i use msg_textbox is called 'Jugaad'
        msg_card= MDCard(
            size_hint=[None,None],
            size=[sizeX,sizeY],
            padding=20,
            elevation=9,
            ripple_behavior= True,
            radius= [25,25,0,25 ],
        )
        
        msg_card.add_widget(MDLabel(
            text= msg_data,
            theme_text_color= "Primary",
            size_hint_y= None,
            height= 30
        ))        
        msg_card.md_bg_color = [236/255.0,156/255.0,247/255.0,1]
        self.ids.all_msgs.add_widget(msg_card)
        self.ids.all_msgs.add_widget(text_msg)
        self.ids.msg_scroll_view.scroll_to(msg_card)
        self.ids.msg_textbox.text=""
        date = datetime.date.today()
        date = str(date)
        time = i
        self.update_database(date,time,msg_data)
    def update_database(self,date,time,msg):
        msg_o = msg+'0'
        # https://pmca-a03a7-default-rtdb.firebaseio.com/9594897959/chats/9930253216
        # file = {
        #         date : {time: msg}
        #         }
        print(msg)
        same_date = {
                date + time: msg_o
                }
        try:
            """
            # This is if the chat data is separated by date
            if date == self.check_set:
                print("i am going to requests")
                requests.patch(self.url_date,json = same_date)
                # UrlRequest(url=url,req_body=file,on_success=print("data transfer"))
            else:
                """
            requests.patch(self.url,json = same_date)
            # write a code to save or send the same msg to RXer
            self.RXer_update(date,time,msg)
            # RXer code ends here
            self.parent.Bottom_msg("Updated")
        except requests.exceptions.RequestException as e:
            print("---From Upadte_database---",self.url)
            self.search_chat_room(self.chat_room_no)
            s_url ="https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats/"+self.chat_room_no+"/.json"
            requests.patch(s_url,json = same_date)  
            self.RXer_update(date,time,msg)
            self.parent.Bottom_msg("Please Turn On Internet..")
        self.refresh_chat_data()
    def RXer_update(self,date,time,msg):
        """
        This function Helps to reflect same msg to other side
        """
        msg_r = msg+"1"
        r_chat = requests.get("https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.chat_room_no+"/chats/.json")
        print()
        if r_chat.ok==True and r_chat.json() == "None":
            patch={
                    date + time: msg_r
                }
            data = {
                self.owner_no:patch
            }
            c_url = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.chat_room_no+"/chats/.json"
            requests.patch(c_url,json = data)
        elif r_chat.ok == True and self.owner_no in r_chat.json().keys():
    
            url = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.chat_room_no+"/chats/"+self.owner_no+"/.json"
            data_d = {
                date + time: msg_r
            }
            requests.patch(url,json = data_d)
            
            # json_data = r_chat.json()
            
    def res(self,*args):
        print("Result: after success", self.check.result.keys())
        for c in  self.check.result.keys():
            self.check_set.add(c)
        print(self.check_set)

    def refresh_chat_data(self):
        try:
            file = requests.get('https://pmca-a03a7-default-rtdb.firebaseio.com/'+self.owner_no+'/chats.json')
            data = file.json()
            try:
                with open('ChatHub.json','w') as C:
                    json.dump(data,C)
            except FileExistsError:
                print("file is exist ")
        except requests.exceptions.RequestException:
            self.parent.Bottom_msg("Please Turn On Internet..")
    def rx_msg(self,msg_data,i):
        """
            This recieves msg from data base or local file 
        """
        print(" i am in recieved msg",msg_data[-1])


        msg_data = msg_data[0:len(msg_data)-1] # this is Msg
        text_msg = MDLabel(text=i,theme_text_color="Hint",font_style="Overline",halign= "left")        
        sizeX = self.ids.msg_textbox.size[0] 
        sizeY = self.ids.msg_textbox.size[1]
        # ->> sizeY is equal to msg_textbox sizeY because text_msg sizeY not work 
        # that's why i use msg_textbox is called 'Jugaad'
        msg_card= MDCard(           
            size_hint=[None,None],
            size=[sizeX,sizeY],
            padding=20,
            elevation=9,
            ripple_behavior= True,
            radius= [25,25,25,0 ],
        )
        msg_card.add_widget(MDLabel(
            text= msg_data,
            theme_text_color= "Primary",
            size_hint_y= None,
            height= 30
        ))
        
        msg_card.md_bg_color = [182/255,244/255,109/255,1]
        self.ids.all_msgs.add_widget(msg_card)
        self.ids.all_msgs.add_widget(text_msg)
        self.ids.msg_scroll_view.scroll_to(msg_card)
        self.ids.msg_textbox.text=""
    def search_chat_room(self,number):
        # Use this fuction for search chat room or blank chat room
        self.u_url = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats/.json"        

        data = {
            number : " "
        }
        requests.patch(self.u_url,json = data)
        
        print("This is the search chat_room of ",number)

    def feachers(self):
        """
        method call when plus btn click .
        
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
                lambda x, y=item[0]: print("not now"), #self.parent.get_screen("profile").file_manager_open(),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()
    def on_leave(self, *args):
        self.ids.all_msgs.clear_widgets()
        url1 = "https://pmca-a03a7-default-rtdb.firebaseio.com/"+self.owner_no+"/chats.json"        
        try:
            all_chats = requests.get(url1)
            chats_data = all_chats.json()
            with open('ChatHub.json','w') as C:
                json.dump(chats_data,C)
        except requests.exceptions.RequestException:  # This is the correct syntax
            # Offline code goes here.. Load the ChatHub.json file to Screen
            print("You are Offline")              