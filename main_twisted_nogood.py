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

from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.print_message(data)


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        self.app.print_message("connection failed")


class MyApp(App):
    connection = None
    host = '192.168.56.1'
    port = 8000

    def build(self):
        wid = Widget()

        label = Label(text='empty')
        button = Button(text='Connect...', on_press=partial(self.connect, label))
        textbox = TextInput(size_hint_y=.1, multiline=False)
        textbox.bind(on_text_validate=self.send_message)
        layout = BoxLayout()
        layout.add_widget(label)
        layout.add_widget(button)
        layout.add_widget(textbox)

        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)

        return root

    def connect(self, label, *largs):
        self.connect_to_server()

    def connect_to_server(self):
        reactor.connectTCP(self.host, self.port, EchoFactory(self))

    def on_connection(self, connection):
        self.print_message("connected succesfully!")
        self.connection = connection

    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""

    def print_message(self, msg):
        self.label.text += msg + "\n"

if __name__ == '__main__':
    MyApp().run()