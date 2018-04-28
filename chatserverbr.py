#!/usr/bin/env python3

"""Servidor multithread para aplicação de chat"""

from socket import *
from threading import Thread

def accept_incoming_connections():
    """ Definindo conexões com clientes """
    
    while True:
        client, client_address = SERVER.accept()
        print("%s: %s conectado." % client_address)
        client.send(bytes("Bem-vindo ao IF Chat V0.0.1a! " +
                            "Insira seu apelido e pressione enter.", "utf8"))
        addresses[client] = client_address
        Thread(target = handle_client, args = (client,)).start()

def handle_client(client):  # Pegando o socket do client como argumento
    """Configurando a conexão com um cliente"""
    name = client.recv(BUFFSIZE).decode("utf8")
    welcome = 'Bem-vindo %s! Se deseja sair, digite {sair} para sair.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s entrou na conversa." % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFFSIZE)
        if msg != bytes("{sair}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{sair}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s Saiu da conversa."% name, "utf8"))
            break

def broadcast (msg, prefix = ""):  # Prefixo é para identificar quem fala
    
    #""" Enviar uma mensagem em broadcast para todos """"
    
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+ msg)


clients = {}
addresses = {}

HOST = '192.168.137.87'
PORT = 33000
BUFFSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    SERVER.listen(5)   # Permissão para no máximo 5 conexões simultâneas
    print("Aguardando Conexão...")
    ACCEPT_THREAD = Thread(target = accept_incoming_connections)
    ACCEPT_THREAD.start()  # Iniciando o loop infinito
    ACCEPT_THREAD.join()
    SERVER.close()