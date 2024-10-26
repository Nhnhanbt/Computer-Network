import socket
import threading
import json
from collections import defaultdict
import os
import hashlib
import base64

TRACKER_PORT = 50000
TRACKER_ADDRESS = "127.0.0.1" #Random IP  :vvv
# PROXY_PORT =
# PROXY_ADDRESS = 
LOCAL_SERVER_ADDRESS = "127.0.0.1"
LOCAL_SERVER_PORT = 61001
HOSTNAME = ""

PIECE_SIZE = 524288  # 524288 byte = 512KB

online = True # Determine srever_thread is running or not

def send_with_retry(tracker_conn, data, timeout = 2, max_retries = 3):
    retries = 0
    while retries < max_retries:
        try:
            # print(data)
            tracker_conn.sendall(json.dumps(data).encode() + b'\n')
            tracker_conn.settimeout(timeout)
            response = tracker_conn.recv(4096).decode()
            response = json.loads(response)
            print(response)
            tracker_conn.settimeout(None)  # Reset timeout
            return response  # If successful, return the received data
        except socket.timeout:
            retries += 1
            print(f"Timeout occurred, retrying {retries}/{max_retries}...")
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # Exit on other errors
        finally:
            print("[TEST] Function send_with_retry run ok")
    
    return None  # If max retries reached, return None

def hash_piece(piece):
    sha256 = hashlib.sha256()  # Using SHA-256 instead of SHA-1
    sha256.update(piece)
    return sha256.digest()

def create_pieces_string(path):
    with open(path, "rb") as data:
        piece_data = data.read()
        hashed_piece = hash_piece(piece_data)
        
        # Convert bytes to a base64-encoded string
        return base64.b64encode(hashed_piece).decode('utf-8')

def send_piece_to_tracker(tracker_conn, publish_order, file_name, file_size, hashes, piece_size):
    global HOSTNAME
    global LOCAL_SERVER_ADDRESS
    global LOCAL_SERVER_PORT
    
    for i in publish_order: # 1 2
        data = {
            "option": "publish",
            "IP": LOCAL_SERVER_PORT,
            "port": LOCAL_SERVER_PORT,
            "hostname": HOSTNAME[0],
            "file_name": file_name,
            "file_size": file_size,
            "piece_size": piece_size[i - 1],
            "piece_order": i,
            "piece_hash": hashes[i - 1]
        }
        result = send_with_retry(tracker_conn, data)
    print(f"[TEST] Result = {result}")
    if result:
        print("[PUBLISH] Publish file successful")
    print("[TEST] Function send_piece_to_tracker run ok")

def get_publish_input(size):
    while True:
        inp = input("Input piece order to publish:").split()
        if not inp:
            continue
        try:
            inp = [int(i) for i in inp]
            if all(0 < i <= size for i in inp) and len(inp) == len(set(inp)):
                return inp
            else:
                print(f"All numbers must be unique and between 1 and {size}. Please try again.")
        except ValueError:
            print("Please enter valid integers.")

def split_file(file_name, size = PIECE_SIZE):
    result = []
    counter = 1
    with open(file_name, "rb") as file:
        for piece_data in iter(lambda: file.read(size), b''):
            piece_file_path = f"{file_name}_piece{counter}"
            with open(piece_file_path, "wb") as piece_file:
                piece_file.write(piece_data)
            result.append(piece_file_path)
            counter += 1
    return result

def check_local_files(file_name):
    if not os.path.exists(file_name):
        return False
    else:
        return True

# Function to select the best destination based on piece_order and priority
def select_destination_by_order(destinations):
    grouped_by_order = defaultdict(list)
    for dest in destinations:
        grouped_by_order[dest['order']].append(dest)
    selected_destinations = []
    # Sort by priority and select the destination with the lowest prio for each order
    for order, group in grouped_by_order.items():
        group = sorted(group, key=lambda x: x['prio'])
        selected_destinations.append(group)
    
    return selected_destinations

# Function to send and receive data via socket
def send_receive_data(ip, port, message="Hello"):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout (in case the destination is unreachable)
        s.settimeout(5)
        # Connect to the server
        s.connect((ip, port))
        # Send data
        print(f"Sending data to {ip}:{port}")
        s.sendall(message.encode())
        # Receive data
        response = s.recv(1024)
        print(f"Received response: {response.decode()} from {ip}:{port}")
        # Close the connection
        s.close()
        return True  # If send/receive was successful
    except (socket.timeout, socket.error) as e:
        print(f"Connection to {ip}:{port} failed: {e}")
        return False  # If send/receive failed

# Main function to handle sending data to the best destination
def send_requests(destinations):
    print("[TEST] Function send_requests start")
    selected_groups = select_destination_by_order(destinations)

    for group in selected_groups:
        for dest in group:  # Try each destination in order of priority
            success = send_receive_data(dest['IP'], dest['port'])
            if success:
                print(f"[TEST] Successfully communicated with {dest['host']} (IP: {dest['IP']}) for order {dest['order']}")
                break  # Stop trying other destinations for this order
            else:
                print(f"[TEST] Failed to communicate with {dest['host']} (IP: {dest['IP']}) for order {dest['order']}, trying next priority.")

def add_priority(data):
    print("[TEST] Function add_priority start")
    prio = {}
    for tmp in data:
        host_id = tmp['piece_order']
        if host_id not in prio:
            prio[host_id] = 0
        else:
            prio[host_id] += 1
        tmp['prio'] = prio[host_id]
        del tmp['ID']
    sorted_result = sorted(data, key=lambda x: (x['piece_order'], x['prio']))
    print("[TEST] Function add_priority run ok")
    print("Sorted peers info:")
    for peer in sorted_result:
        print(f"Piece {peer['piece_order']} stores at {peer['hostname']} ({peer['IP']}, {peer['port']})\n")
    return sorted_result

def publish(tracker_conn):
    file_name = input("Input file name: ")
    is_exist = check_local_files(file_name)
    if is_exist:
        file_size = os.path.getsize(file_name)
        pieces = split_file(file_name)
        hashes = []
        piece_size = []
        for piece in pieces:
            print(f"Piece {pieces.index(piece) + 1}: {piece}")
            hashes.append(create_pieces_string(piece))
            piece_size.append(os.path.getsize(piece))
            # print(piece)
        publish_order = get_publish_input(len(pieces))
        send_piece_to_tracker(tracker_conn, publish_order, file_name, file_size, hashes, piece_size)
        # print(pieces)
        # print(hashes)
        # print(publish_order)
    else :
        print("[PUBLISH] File not exist")

def ping():
    print("ping")

def download(tracker_conn, file_name):
    try:
        # Check local info of requested file
        pieces = local_pieces(file_name)
        hashes = hash_local_piece(pieces)
        piece_order = local_piece_order(file_name)
        
        # Send to tracker to request for peers info
        data = {
            "file_name": file_name,
            "piece_hash": hashes,
            "piece_order": piece_order
        }
        metainfo = send_with_retry(tracker_conn, data)
        peers = metainfo['metainfo']
        if metainfo is not None:
            print("[DOWNLOAD] Successfully received metainfo")
        else:
            print("[DOWNLOAD] Failed to receive metainfo after retries.")
            return 
        sorted = add_priority(peers)
        send_requests(sorted)
    except Exception as error:
        print("[ERROR] Function download error")
    finally:
        print("[TEST] Function download run ok")

def send_file(conn, addr):
# When threads run this function <=> Some peer request pieces
    try:
        peer_data = conn.recv(4096).decode()
        peer_data = json.loads(peer_data)
        # Not completed
    except Exception as error:
        print("[ERROR] Function send_file error")
    finally:
        conn.close()

def server_main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP/IP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Config: can reuse IP immediately after closed
    server_socket.bind((LOCAL_SERVER_ADDRESS, LOCAL_SERVER_PORT))
    server_socket.listen()

    threads = []
    while online:
        try:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=send_file, args=(conn, addr))
            thread.start()
            threads.append(thread)
        except Exception as error:
            print("[ERROR] Function server_main error")
            break

    for thread in threads:
        thread.join()
    server_socket.close()

def connect_to_tracker(email = "email", password = "password"):
    global HOSTNAME
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TRACKER_ADDRESS, TRACKER_PORT))
    sock.sendall(json.dumps({'email': email, 'password': password}).encode() + b'\n')
    
    result = sock.recv(4096).decode()
    result = json.loads(result)
    status = result['status']
    HOSTNAME = result['hostname']
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
        while True:
            command = input("Input command (download/ping/publish/exit):")
            if(command == "download"):
                file_name = input("Input file name to download: ")
                download(tracker_conn, file_name)
            elif(command == "ping"):
                ping()
            elif(command == "publish"):
                publish(tracker_conn)
            elif(command == "exit"):
                # Remember to close all the conn and join all thread
                # Just in case
                os._exit(0)
                online = False
                server_thread.join()
                
    else:
        print("Login again")