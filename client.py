import socket
from _thread import *

udp_port = 17

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Соединение с сервером разорвано")
            break

def receive_udp_notes(udp_socket):
    while True:
        try:
            message, _ = udp_socket.recvfrom(1024)
            print(f"\n{message.decode('utf-8')}")
        except:
            break

def client_start(ip, server_port, tcp_port, client_ip):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client_sock.bind((client_ip, tcp_port))
            break
        except:
            print("порт уже занят, попробуйте другой")
            tcp_port = int(input("Введите другой порт: "))
    try:
        client_sock.connect((ip, server_port))
        print(f"{client_ip} подключился к серверу {ip}")
        start_new_thread(receive_messages, (client_sock, ))
        
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.bind(("", udp_port))
        start_new_thread(receive_udp_notes,(udp_socket, ))
       
        while True:
            message = input()
            client_sock.send(message.encode("utf-8"))
    except Exception as e:
        print(f"ошибка: {e}")
        print("Соединение потеряно")
    finally:
        try:
            client_sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        client_sock.close()

if __name__ == '__main__':
    ip = input("Введите ip сервера: ")
    tcp_port = int(input("Введите tcp порт клиента: "))
    server_port = int(input("Введите порт сервера: "))
    client_ip = input("Введите ip клиента: ")
    client_start(ip, server_port, tcp_port, client_ip)