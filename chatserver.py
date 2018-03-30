#!/usr/bin/env python3

""" Server multithread for chat app -- Servidor multitread para aplicação de chat"""

from socket import *
from threading import Thread

def accept_incoming_connections():
    """ Setup conexions whit clients -- Definindo conexões com clientes """
    
    while True:
        client, client_address = SERVER.accept()
        print("%s: %s connected." % client_address)
        client.send(bytes("Greetings from the batcave!" +
                            "Now, type you nick and press enter", "utf8"))
        addresses[client] = client_address
        Thread(target = handle_client, args = (client,)).start()

def handle_client(client):  # Takes client socket as argument -- pegando o socket do client como argumento
    """ Handles a single client connection -- Configurando a conexão com um cliente"""
    name = client.recv(BUFFSIZE).decode("utf8")
    welcome = 'Welcome %s! If you ever want quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFFSIZE)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat."% name, "utf8"))
            break

def broadcast (msg, prefix = ""):  #prefix is for name identification -- prefixo é para identificar quem fala
    
    #""" Broadcasts a message to all the clients -- Enviar uma mensagem em broadcast para todos """"
    
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+ msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFFSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(5)   #Listen for 5 conections at max -- permita no m[aximo 5 conexões
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target = accept_incoming_connections)
    ACCEPT_THREAD.start()  #Start the infinite loop -- iniciando o loop infinito
    ACCEPT_THREAD.join()
    SERVER.close()
    