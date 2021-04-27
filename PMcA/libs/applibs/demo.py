from kivy.app import App
#kivy.require("1.9.1")
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest

class MyWidget(BoxLayout):
    def __init__(self,**kwargs):
        super(MyWidget,self).__init__(**kwargs)
        search_url = "https://pmca-a03a7-default-rtdb.firebaseio.com/9594897959/chats/9930253216/"
        print(search_url)
        file= {"4:00":"MI hay koli "}
        self.request = UrlRequest(search_url, req_body= file, on_success=self.res)
        print(self.request)
        print("Result: before success", self.request.result,"\n")


    def res(self,*args):
        print("Result: after success", self.request.result.keys())
        # for c in  self.request.result.keys():
        #     if c == 'cod':
        #         print("REsult -->",c)
        #     else:
                # print("wrong ", c)


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()