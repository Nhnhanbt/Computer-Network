import socket
import threading
import json
from collections import defaultdict

TRACKER_PORT = 50000
TRACKER_ADDRESS = "127.0.0.1" #Random IP  :vvv
# PROXY_PORT =
# PROXY_ADDRESS = 
CLIENT_PORT = 61000
LOCAL_SERVER_ADDRESS = "127.0.0.1"
LOCAL_SERVER_PORT = 61001

online = True

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

def send_with_retry(tracker_conn, data, timeout = 2, max_retries = 3):
    retries = 0
    while retries < max_retries:
        try:
            tracker_conn.sendall(json.dumps(data).encode() + b'\n')
            tracker_conn.settimeout(timeout)
            metainfo = json.loads(tracker_conn.recv(4096).decode())
            tracker_conn.settimeout(None)  # Reset timeout
            return metainfo  # If successful, return the received data
        except socket.timeout:
            retries += 1
            print(f"Timeout occurred, retrying {retries}/{max_retries}...")
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # Exit on other errors
        finally:
            print("TEST Function send_with_retry run ok")
    
    return None  # If max retries reached, return None

def publish():
    print("publish")

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
            print("Successfully received metainfo")
        else:
            print("Failed to receive metainfo after retries.")
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
            elif(command == "ping"):
                ping()
            elif(command == "publish"):
                publish()
            elif(command == "exit"):
                # Remember to close all the conn and join all thread
                # Just in case
                online = False
        server_thread.join()
    else:
        print("Login again")