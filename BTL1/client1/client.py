import socket
import threading
import json

TRACKER_PORT = 50000
TRACKER_ADDRESS = "127.0.0.1" #Random IP  :vvv
# PROXY_PORT =
# PROXY_ADDRESS = 
CLIENT_PORT = 61000
LOCAL_SERVER_ADDRESS = "127.0.0.1"
LOCAL_SERVER_PORT = 61001

online = True

def request_for_piece(des):
    print("[TEST] Function choose_peers run ok1")

def choose_peers(peers):
    print("[TEST] Function choose_peers run ok1")
    print("Choosing destination peers...")
    for peer in peers:
        print(f"Piece {peer['piece_order']} stores at {peer['hostname']} ({peer['IP']}, {peer['port']})\n")

def download(tracker_conn, file_name):
    try:
        # Check local info of requested file
        pieces = local_pieces(file_name)
        hashes = hash_local_piece(pieces)
        piece_order = local_piece_order(file_name)
        
        # Send to tracker to request for peers info
        # Resend
        tracker_conn.sendall(json.dumps({
            "file_name": file_name,
            "piece_hash": hashes,
            "piece_order": piece_order
        }).encode() + b'\n')

        # Receive peers info
        metainfo = json.loads(tracker_conn.recv(4096).decode())
        peers = metainfo['metainfo']
        destination_peers = choose_peers(peers)
        request_for_piece(destination_peers)
    except Exception as error:
        print("[ERROR] Function download error")
    finally:
        print("[TEST] Function download run ok")


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
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Config: can reuse IP immediately after closed
    server_socket.bind((LOCAL_SERVER_ADDRESS, LOCAL_SERVER_PORT))
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
        print("[TEST] Function connect_to_tracker run ok1")
        return sock
    else :
        print("[TEST] Function connect_to_tracker run ok2")
        return None

if __name__ == "__main__":
    # login first
    email = "myemail"
    password = "mypassword"
    tracker_conn = connect_to_tracker(email, password)
    if tracker_conn:
        server_thread = threading.Thread(target=server_main)
        server_thread.start()
        while online:
            command = input()
            if(command == "download"):
                file_name = input()
                download(tracker_conn, file_name)
            # elif(command == "ping"):
            #     ping()
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
    