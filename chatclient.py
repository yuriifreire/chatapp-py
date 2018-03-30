#!/usr/bin/env python3
""" Script for chat client using Tkinter -- Scritp para o chat usando TK """

from socket import *
from threading import Thread
import tkinter

def receive():
    """" Handles receive of messages -- Configurando o recebimento de menssagens """
    while True:
        try:
            msg = client_socket.recv(BUFFSIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  #Possibly client has left the chat -- Quando der esse erro, possivelmente o cliente deslogou
            break

def send(event = None): #Event is pass by binders -- evento sera passado por bind (botao)
    """" Handles sendig of messages -- Configurando o envio de mensagens """
    msg = my_msg.get()
    my_msg.set("")  #Clear input filed - limpar o campo de texto
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event = None):
    """This functions is called when the window is closed -- Essa função é chamada quando a janela é fechada"""
    my_msg.set("{quit}")
    send()

top = tkinter.Tk()
top.title("Chat App - ADEY")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  #For can send messages -- Para poder enviar as mensagens
my_msg.set("Type your message here.")
scrollbar = tkinter.Scrollbar(messages_frame)  #To navigate through past messages - Pra ver as mensagens anteriores

#Following will contain the messages.  -- Abaixo armazenará as mensagens

msg_list = tkinter.Listbox(messages_frame, height = 15, width = 50, yscrollcommand = scrollbar.set)
scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)
msg_list.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable = my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text = "Send", command = send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#---Now comes the socket part -- Vamos começar a parte dos sockets---

HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFFSIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target = receive)
receive_thread.start()
tkinter.mainloop()  #Starts GUI execution -- Iniciar a interface gráfica