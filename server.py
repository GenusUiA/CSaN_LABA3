import socket
from _thread import *

udp_port = 17

def tcp_client_messages(client_sock, client_ip, clients, server_socket_udp):
    while True:
        try:
            message = client_sock.recv(1024).decode("utf-8")
            if not message:
                break
            print(f"Сообщение от {client_ip}")
            for client in list(clients):
                try:
                    if client != client_sock:
                        client.send(f"{client_ip}: {message}".encode('utf-8'))
                except:
                    continue  
        except ConnectionResetError:
            break
    leave_message = f"Пользователь отошел от дел: {client_ip}"
    print(leave_message)
    try:
        if client_sock in clients:
            clients.remove(client_sock)
        server_socket_udp.sendto(leave_message.encode("utf-8"), ("<broadcast>", udp_port))
    except:
        pass
    try:
        client_sock.shutdown(socket.SHUT_RDWR)
    except:
        pass
    client_sock.close()
    
def start_server(server_ip, server_tcp_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients = []
    try:
        server_socket.bind((server_ip, server_tcp_port))
    except OSError:
        return
    server_socket.listen(5)
    print(f"Сервер запущен на {server_ip}, tcp_port: {server_tcp_port}, udp_port: {udp_port}")
    server_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        server_socket_udp.bind((server_ip, udp_port))
    except OSError as e:
        print(f"Ошибка: порт {server_tcp_port} недоступен. Причина: {e}")
        return  
    try:
        while True:
            client_socket, (client_ip, _) = server_socket.accept()
            clients.append(client_socket)
            start_message = f"Новый пользователь: {client_ip}"
            server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            server_socket_udp.sendto(start_message.encode("utf-8"), ("<broadcast>", udp_port))
            start_new_thread(tcp_client_messages, (client_socket, client_ip, clients, server_socket_udp))
    finally:
        server_socket_udp.close()
        try:
            server_socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        server_socket.close()        
    
if __name__ == "__main__":
    server_ip = input("Введите ip сервера: ")
    server_tcp_port = int(input("Введите tcp_порт сервера: "))
    start_server(server_ip, server_tcp_port)
     