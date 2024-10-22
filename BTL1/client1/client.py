import socket
import threading
import json

TRACKER_PORT = 50000
TRACKER_ADDRESS = "127.0.0.1" #Random IP  :vvv
# PROXY_PORT =
# PROXY_ADDRESS = 
CLIENT_PORT = 61000

online = True

def send_file(conn, addr):
# When threads run this function <=> Some peer request pieces
    try:
        peer_data = conn.recv(4096).decode()
        peer_data = json.loads(peer_data)
    except Exception as error:
        print("[ERROR] Function send_file error")
    finally:
        conn.close()

def server_main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP/IP
    server_socket.bind((TRACKER_ADDRESS, TRACKER_PORT))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Config: can reuse IP immediately after closed
    server_socket.listen()

    while online:
        try:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=send_file, args=(conn, addr))
            thread.start()
        except Exception as error:
            print("[ERROR] Function server_main error")
            break
    server_socket.close()

def connect_to_tracker(email = "email", password = "password"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TRACKER_ADDRESS, TRACKER_PORT))
    sock.sendall(json.dumps({'email': email, 'password': password}).encode() + b'\n')
    
    result = sock.recv(4096).decode()
    result = json.loads(result)
    status = result['status']

    if status:
        print("[TEST] Function connect_to_tracker run ok")
        return sock
    else :
        return None

if __name__ == "__main__":
    # login first
    email = "myemail"
    password = "mypassword"
    tracker_conn = connect_to_tracker(email, password)
    # if tracker_conn:
    #     server_thread = threading.Thread(target=server_main)
    #     server_thread.start()
    #     while online:
    #         command = input()
    #         if(command == "get-info"):
    #             get_file_part_list()
    #         elif(command == "ping"):
    #             ping()
    #         elif(command == "upload"):
    #             upload()
    #         elif(command == "publish"):
    #             publish()
    #         elif(command == "download"):
    #             download()
    #         elif(command == "exit"):
    #             # Remember to close all the conn and join all thread
    #             # Just in case
    #             online = False
    # else:
    #     print("Login again")   
    