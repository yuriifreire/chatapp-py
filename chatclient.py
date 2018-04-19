
#!/usr/bin/env python3
""" Script para o cliente de chat usando TKinter """

from socket import *
from threading import Thread
import tkinter

def receive():
    """" Configurando o recebimento de menssagens """
    while True:
        try:
            msg = client_socket.recv(BUFFSIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Quando der esse erro, possivelmente o cliente deslogou
            break

def send(event = None): # Evento sera passado por bind (botao)
    """" Configurando o envio de mensagens """
    msg = my_msg.get()
    my_msg.set("")  # Limpar o campo de texto
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{sair}":
        client_socket.close()
        top.quit()

def on_closing(event = None):
    """Essa função é chamada quando a janela é fechada"""
    my_msg.set("{sair}")
    send()

top = tkinter.Tk()
top.title("IFChat V0.0.1a")

top.configure(bg="#ffff99")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # Para poder enviar as mensagens
my_msg.set("Digite sua mensagem aqui.")
scrollbar = tkinter.Scrollbar(messages_frame)  # Para ver as mensagens anteriores
scrollbar.configure(bg="#ffff99")

# Abaixo armazenará as mensagens

msg_list = tkinter.Listbox(messages_frame, height = 15, width = 60, yscrollcommand = scrollbar.set)
scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)
msg_list.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
msg_list.configure(bg="#ffff99", fg="#0000cc", highlightbackground="#666699")
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable = my_msg)
entry_field.bind("<Return>", send)
entry_field.configure(bg="#ffff99", fg="#0000cc", relief="ridge", highlightbackground="#666699")
entry_field.pack()
send_button = tkinter.Button(top, text = "Enviar", command = send)
send_button.configure(bg="#ffff99", fg="#0000cc", relief="raised", highlightbackground="#666699")
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#--- Vamos começar a parte dos sockets ---

HOST = input('Host: ')
PORT = input('Port: ')

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
tkinter.mainloop()  # Iniciar a interface gráfica
