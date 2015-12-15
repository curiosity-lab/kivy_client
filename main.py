import kivy
kivy.require('1.9.0')  # replace with your current kivy_tests version !
from kivy.app import App
from kivy.graphics import *
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from functools import partial
import socket


class MyApp(App):
    connection = None
    server_list = ['192.168.1.102', '192.168.1.101', '192.168.1.1']
    port = 12345

    def build(self):
        wid = Widget()

        label = Label(text='')
        button = Button(text='Connect...', on_press=partial(self.connect, label))
        textbox = TextInput(size_hint_y=.1, multiline=False)
        textbox.bind(on_text_validate=partial(self.send_message, textbox, label))
        layout = BoxLayout()
        layout.add_widget(label)
        layout.add_widget(button)

        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)

        return root

    def connect(self, label, *largs):
        self.connection = socket.socket()
        for server in self.server_list:
            try:
                print(server)
                h = socket.gethostbyaddr(server)
                print(h)
                try:
                    print(h[0])
                    self.connection.connect((h[2][0], self.port))
                    label.text += "Connected to " + server + '\n'
                    #self.print_message(str(self.connection.recv(1024)), label)
                    break
                except:
                    label.text += "Error. Cannot connect" + '\n'
            except:
                label.text += "Error. " + server + '\n'
        try:
            self.connection.connect(('Goren-PC', self.port))
            label.text += "Connected to goren-PC \n"
        except:
            label.text += "Last error."

    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.connection = connection

    def send_message(self, textbox, label, *args):
        msg = textbox.text
        if msg and self.connection:
            self.connection.send(textbox.text.encode())
            msg = self.connection.recv(1024)
            self.print_message(msg, label)

    def print_message(self, msg, label):
        label.text += str(msg) + "\n"

if __name__ == '__main__':
    MyApp().run()