import socket
import time

def is_host_online(host):
    port = 80
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        if result == 0:
            print("The server is online.\n")
            return "The server is online."
        else:
            print("The server is offline.\n")
            return "The server is offline."

    except socket.error as e:
        return "An error occurred while checking the server status: {}".format(e)

    finally:
        sock.close()


def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        sock.connect((host, port))
        try:
            service_name = socket.getservbyport(port, 'tcp')
        except OSError:
            service_name = "Unknown"
        print(f"{host} is online on port {port}({service_name})")

    except socket.error:
        print(f"{host} is offline")
        return True
    finally:
        sock.close()

def delay(host, port, rcnt):
    tdel = 0
    for d in range(rcnt):
        start_time = time.time()
        try:
            with (socket.create_connection((host, port), timeout=2)):
                tdel += time.time() - start_time
        except (socket.timeout, socket.error):
            pass
        avgdel = tdel/rcnt * 1000
        avgdel = int(avgdel)
    print(f"{avgdel} ms")

def send_get_request(host, port, user_in):
    port = int(port)
    request = f"GET {user_in}"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    message = request
    client.send(message.encode())
    response = client.recv(1024).decode()
    print(response)

def post_user_to_server(port, host, user_data):
    port = int(port)
    request = f"POST {user_data}"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(request.encode())
    response = client_socket.recv(1024).decode()
    print(response)

Host = 'localhost'
Port = 8080
server_url = Host + ':' + Host

while True:

    user_input = input()
    if 'CHECK' in user_input:
        is_host_online(input("Enter host : "))
    if 'PORTS' in user_input:
        host = input("Enter host : ")
        sport = int(input("Enter start port : "))
        eport = int(input("Enter end port : "))
        for port in range(sport, eport+1):
            check_port(host, port)
    if 'GET' in user_input:
        id = input("Enter user id : ")
        send_get_request('localhost', 8080, id)
    if 'POST' in user_input:
        idd = input("Enter user name + user age : ")
        post_user_to_server(Port, Host, idd )
    if 'DELAY' in user_input:
        host = input("Enter host : ")
        port = int(input("Enter port : "))
        rcnt = int(input("Enter request count : "))
        delay(host, port, rcnt)