import socket
import threading
import mysql.connector as mysql
import json

TRACKER_PORT = 50000
TRACKER_ADDRESS = "127.0.0.1" #Random IP  :vvv

con = mysql.connect(host="localhost", user="root", password="", database="computer_network")
cursor=con.cursor()
# cursor.execute("Some query"")

def client_handler(conn, addr):
    login(conn, addr)


def login(conn, addr):
    try:
        while True:
            login_info = conn.recv(4096).decode()
            if (not login_info):
                print("[LOGIN] Missing email/password")
                conn.sendall(json.dumps({'status': False}).encode())
                return False
            else :
                login_info = json.loads(login_info)
                email = login_info['email']
                password = login_info['password']
                cursor.execute("SELECT hostname FROM login WHERE email = %s AND password = %s", (email, password))
                successfull = cursor.fetchall()
                if successfull:
                    for hostname in successfull: peer_info = {'status': True, 'hostname': hostname}
                    conn.sendall(json.dumps(peer_info).encode())
                    return True
                else :
                    conn.sendall(json.dumps({'status': False}).encode())
                    return False
    except Exception as error:
        print("[ERROR] Function login error")
    finally:
        # erase info of this conn in table peers before close connection
        print("[LOGIN] Function login run ok")

def server_main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP/IP
    server_socket.bind((TRACKER_ADDRESS, TRACKER_PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on PORT = {TRACKER_PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"[ACCEPT] Connected to clients throught {conn.getsockname()}")
            print(f"[ACCEPT] Client socket: {addr}")
            thread = threading.Thread(target=client_handler, args=(conn, addr))
            # print("[TEST] Finding bug")
            thread.start()
            print(f"[SERVER] Active connections: {threading.active_count() - 1}")
            thread.join()
            print("[TEST] Finding bug")

    except Exception as error:
            print(error)
    finally:
        server_socket.close()
        cursor.close()

if __name__ == "__main__":
    server_thread = threading.Thread(target=server_main)
    server_thread.start()
    server_thread.join()