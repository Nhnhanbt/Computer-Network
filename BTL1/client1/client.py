import socket
import threading
import json, os
import random
from collections import defaultdict
import os
import hashlib
import base64
import time

TRACKER_PORT = 50000
TRACKER_ADDRESS = "127.0.0.1" #Random IP  :vvv
# PROXY_PORT =
# PROXY_ADDRESS = 
LOCAL_SERVER_ADDRESS = "127.0.0.1"
LOCAL_SERVER_PORT = 61001
HOSTNAME = ""

PIECE_SIZE = 524288  # 524288 byte = 512KB
# public_key_server = None
# PUBLIC_KEY = None
# PRIVATE_KEY = None
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
            # print(response)
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

def verify_piece(actual_hash, expected_hash):
    # Compare with the expected hash
    if actual_hash == expected_hash:
        print(f"[SECURITY] Piece is valid.")
        return True
    else:
        print(f"[SECURITY WARNING] Piece is corrupt.")
        return False

def send_piece_to_tracker(tracker_conn, publish_order, file_name, file_size, hashes, piece_size):
    global HOSTNAME
    global LOCAL_SERVER_ADDRESS
    global LOCAL_SERVER_PORT
    
    for i in publish_order: # 1 2
        data = {
            "option": "publish",
            "IP": LOCAL_SERVER_PORT,
            "port": LOCAL_SERVER_PORT,
            "hostname": HOSTNAME,
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

def split_file(path, file_name, size = PIECE_SIZE):
    result = []
    counter = 1
    with open(path, "rb") as file:
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
    print("[TEST] Function select_destination_by_order start")
    grouped_by_order = defaultdict(list)
    # print(destinations)
    for dest in destinations:
        grouped_by_order[dest['piece_order']].append(dest)
    selected_destinations = []
    # Sort by priority and select the destination with the lowest prio for each order
    for order, group in grouped_by_order.items():
        group = sorted(group, key=lambda x: x['prio'])
        selected_destinations.append(group)
    print("[TEST] Function select_destination_by_order run ok")
    return selected_destinations

# Function to send and receive data via socket
def send_receive_data(ip, port, file_name, piece_order):
    print("[TEST] Function send_receive_data start")
    try:
        port = int(port)
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout (in case the destination is unreachable)
        s.settimeout(5)
        # Connect to the server
        s.connect((ip, port))

        # Send the request as JSON
        print(f"Sending data to {ip}:{port}")
        request = json.dumps({
            'option': 'download',
            'file_name': file_name,
            'piece_order': piece_order
        }).encode('utf-8')
        s.sendall(request + b'\n')  # Append newline to indicate end of message

        # Open file to write the received data
        with open(f"{file_name}_piece{piece_order}", 'wb') as f:
            while True:
                data = s.recv(4096)  # Receive data in chunks
                if not data:
                    break  # Exit loop if no more data
                f.write(data)  # Write the chunk to the file

        print(f"[DOWNLOAD] Received piece {piece_order} from {ip}:{port}")
        return True
    except (socket.timeout, socket.error) as e:
        print(f"Connection to {ip}:{port} failed: {e}")
        return False  # If send/receive failed
    finally:
        s.close()
        print("[TEST] Function send_receive_data run ok")

def mddt(group):
    print("[MDDT] Function MDDT start")
    # print(group)

    for dest in group:  # Try each destination in order of priority
        # print(dest)
        success = send_receive_data(dest['IP'], dest['port'], dest['file_name'], dest['piece_order'])
        if success:
            print(f"[TEST] Successfully communicated with {dest['hostname']} (IP: {dest['IP']}) for order {dest['piece_order']}")
            break  # Stop trying other destinations for this order
        else:
            print(f"[TEST] Failed to communicate with {dest['hostname']} (IP: {dest['IP']}) for order {dest['piece_order']}, trying next priority.")
    print("[MDDT] Function MDDT run ok")

# Main function to handle sending data to the best destination
def send_requests(destinations):
    print("[TEST] Function send_requests start")
    selected_groups = select_destination_by_order(destinations)

    mddts = []

    for group in selected_groups:
        mddt_thread = threading.Thread(target=mddt, args=(group,))
        mddt_thread.start()
        mddts.append(mddt_thread)
        # for dest in group:  # Try each destination in order of priority
        #     success = send_receive_data(dest['IP'], dest['port'], dest['file_name'], dest['piece_order'])
        #     if success:
        #         print(f"[TEST] Successfully communicated with {dest['hostname']} (IP: {dest['IP']}) for order {dest['piece_order']}")
        #         break  # Stop trying other destinations for this order
        #     else:
        #         print(f"[TEST] Failed to communicate with {dest['hostname']} (IP: {dest['IP']}) for order {dest['piece_order']}, trying next priority.")
    for tmp in mddts:
        tmp.join()
    print("[TEST] Function send_requests run ok")

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
        print(f"Piece {peer['piece_order']} stores at {peer['hostname']} ({peer['IP']}, {peer['port']})")
    print("[TEST] Function add_priority run ok")
    return sorted_result

def publish(tracker_conn):
    path = input("Input path to that file name: ")
    file_name = os.path.basename(path)
    is_exist = check_local_files(path)
    if is_exist:
        file_size = os.path.getsize(path)
        pieces = split_file(path, file_name)
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

def ping(ip, port, request_count=5):
    for i in range(request_count):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))
            message = {
                'option': 'ping',
                'message':f"ping | ICMP_order: {i + 1}"
            }
            print(f"Sending request {i + 1} to {ip}:{port}")
            client_socket.sendall(json.dumps(message).encode())
            client_socket.settimeout(2)
            tmp = client_socket.recv(4096).decode()
            response = json.loads(tmp)
            mess = response['message']
            print(f"Received response {i + 1}: {mess} from {ip}:{port}")
        except socket.timeout:
            print("Request timed out.")
        except Exception as error:
            print(f"[ERROR] Failed to send request {i + 1} to {ip}:{port}: {error}")
        finally:
            client_socket.close()  
        time.sleep(1) 

def ping_handler(conn, addr, data):
    try:
        message = data['message']
        print(f"[INFO] Received ping request from {addr[0]}:{addr[1]}")

        if data['option'] == 'ping':
            icmp_order = data['message'].split(":")[-1].strip()
            response_message = {
                'option': 'pong',
                'message': f"pong | ICMP_order: {icmp_order}"
            }
            conn.sendall(json.dumps(response_message).encode())
        else:
            print(f"[ERROR] Unknown option received: {message['option']}")
    except json.JSONDecodeError as json_error:
        print(f"[ERROR] Failed to decode JSON message from {addr}: {json_error}")
    except Exception as error:
        print(f"[ERROR] Failed to handle request from {addr}: {error}")
    finally:
        conn.close()

def merge_files(file_name, pieces, file_size):
    all_exist = all(os.path.exists(piece) for piece in pieces)
    if not all_exist:
        print("[MERGE] Not enough pieces to merge.")
        return
    total_size = 0
    for piece in pieces:
        total_size += os.path.getsize(piece)
    if total_size != file_size:
        print("[ERROR] Merging files failed: Total size does not match the original file size.")
        return
    with open(file_name, "wb") as file:
        for piece in pieces:
            with open(piece, "rb") as piece_file:
                file.write(piece_file.read())
            #os.remove(piece)
    print(f"[MERGE] Successfully merged {len(pieces)} pieces into {file_name}.")
    return True

def local_pieces(file_name):
    pieces = []
    directory = os.getcwd() 
    all_files = os.listdir(directory)
    
    for filename in all_files:
        if filename.startswith(file_name) and filename[len(file_name)] == '_':
            part = filename[len(file_name) + 1:]
            if part.startswith('piece') and part[5:].isdigit():
                pieces.append(filename)
    
    return pieces if pieces else []

def hash_local_piece(pieces):
    hashes = []
    for piece in pieces:
        hashes.append(create_pieces_string(piece))
    return hashes

def local_piece_order(file_name):
    present_pieces = local_pieces(file_name)
    present_orders = set(int(piece.split("_piece")[-1]) for piece in present_pieces)
    return list(present_orders)

def download(tracker_conn, file_name):
    global HOSTNAME
    try:
        if check_local_files(file_name):
            print("[DOWNLOAD] File already in local")
            return
        # Check local info of requested file
        pieces = local_pieces(file_name)
        hashes = hash_local_piece(pieces)
        piece_order = local_piece_order(file_name)
        
        # print(pieces)
        # print(hashes)
        # print(piece_order)

        # Send to tracker to request for peers info
        data = {
            'option': 'download',
            "file_name": file_name,
            "piece_hash": hashes,
            "piece_order": piece_order,
            "hostname": HOSTNAME
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

        # Security checking
        tmp = local_piece_order(file_name)
        # new_piece_order = list(set(tmp) - set(piece_order))
        new_piece_order = [piece for piece in tmp if piece not in piece_order]
        tmp = local_pieces(file_name)
        new_pieces =  [piece for piece in tmp if piece not in pieces]
        new_hashes = hash_local_piece(new_pieces)

        # print(f"new_piece_order: {new_piece_order}")
        # print(f"tmp: {tmp}")
        # print(f"new_pieces: {new_pieces}")
        # print(f"new_hashes: {new_hashes}")
        for i in peers:
            # print(i)
            # print(new_piece_order)
            if int(i['piece_order']) in new_piece_order:
                # print(i['piece_order'])
                # print(new_piece_order.index(int(i['piece_order'])))
                # print(new_hashes[new_piece_order.index(int(i['piece_order']))] + '\n')
                verify_piece(new_hashes[new_piece_order.index(int(i['piece_order']))], i['piece_hash'])
        file_size = int(peers[0]['file_size'])
        merge_files(file_name, tmp, file_size)
    except Exception as error:
        print(f"[ERROR] Function download {error}")
    finally:
        print("[TEST] Function download run ok")

def send_file(conn, addr, peer_data):
    print(f"[CONNECTION] Accepted connection from {addr}")
    try:
        # Receive the request from the peer
        # peer_data = conn.recv(4096).decode('utf-8').strip()
        # peer_data = json.loads(peer_data)

        piece_name = f"{peer_data['file_name']}_piece{peer_data['piece_order']}"
        if os.path.isfile(piece_name):
            # Send the file content in binary mode
            with open(piece_name, 'rb') as f:
                while True:
                    bytes_read = f.read(4096)  # Read file in 4096-byte chunks
                    if not bytes_read:
                        break  # Exit loop if end of file reached
                    conn.sendall(bytes_read)  # Send the chunk to the client
            print(f"[UPLOAD] Sent piece {peer_data['piece_order']} to {addr}")
        else:
            # If file piece does not exist, send an error message
            error_msg = json.dumps({"error": "Requested file piece not found"}).encode('utf-8')
            conn.sendall(error_msg)
            print(f"[ERROR] File piece {piece_name} not found for {addr}")

    except Exception as error:
        print(f"[ERROR] Function send_file: {error}")
    finally:
        conn.close()
        print(f"[CONNECTION] Closed connection with {addr}")

def server_main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP/IP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Config: can reuse IP immediately after closed
    server_socket.bind((LOCAL_SERVER_ADDRESS, LOCAL_SERVER_PORT))
    server_socket.listen()

    threads = []
    while online:
        try:
            conn, addr = server_socket.accept()
            data = conn.recv(4096).decode()
            data = json.loads(data)
            if data['option'] == 'ping':
                thread = threading.Thread(target=ping_handler, args=(conn, addr, data))
            else:
                thread = threading.Thread(target=send_file, args=(conn, addr, data))
            # thread = threading.Thread(target=send_file, args=(conn, addr))
            thread.start()
            threads.append(thread)
        except Exception as error:
            print(f"[ERROR] Function server_main {error}")
            break

    for thread in threads:
        thread.join()
    server_socket.close()

def connect_to_tracker():
    try :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TRACKER_ADDRESS, TRACKER_PORT))
        if sock:
            print("[CONNECTION] Connected to tracker")
            return sock
        else:
            print("[ERROR] Failed to connect server.")
            return None
    finally:
        print("[TEST] Function connect_to_tracker run ok")
    
def login(conn, email, password):
    try: 
        global HOSTNAME
        data = {
            'option': 'login',
            'email': email, 
            'password': password
        }
        response = send_with_retry(conn, data)
        status = response['status']
        HOSTNAME = response['hostname']
        print(HOSTNAME)
        if status:
            print("[LOGIN] Login successful.")
            return status
        else:
            mes = response['mes']
            print(mes)
            return False
    except Exception as error:
        print("[ERROR] Function signup error:", error)
    finally:
        print("[TEST] Function signup run ok")
    
def signup(conn, email, password):
    try:
        signup_data = {
            'option': 'signup',
            'email': email,
            'password': password
        }
        result = send_with_retry(conn, signup_data)
        status = result['status']
        if status:
            print(f"[SIGNUP] {result['mes']}")
            return True
        else:
            mes = result['mes']
            print(mes)
            return False
    except Exception as error:
        print("[ERROR] Function signup error:", error)
    finally:
        print("[TEST] Function signup run ok")

# def is_prime(num):
#     if num < 2:
#         return False
#     for i in range(2, int(num ** 0.5) + 1):
#         if num % i == 0:
#             return False
#     return True

# def generate_large_prime(min_val=50):
#     prime = random.randint(min_val, min_val * 2)
#     while not is_prime(prime):
#         prime = random.randint(min_val, min_val * 2)
#     return prime
     
# # Modulo inverse
# def mod_inverse(e, phi):
#     d, x1, x2, y1 = 0, 0, 1, 1
#     temp_phi = phi
#     while e > 0:
#         temp1, temp2 = temp_phi // e, temp_phi - temp_phi // e * e
#         temp_phi, e = e, temp2
#         x, y = x2 - temp1 * x1, d - temp1 * y1
#         x2, x1, d, y1 = x1, x, y1, y
#     if temp_phi == 1:
#         return d + phi
#     return None

# # create RSA key
# def generate_keypair():
#     p = generate_large_prime()
#     q = generate_large_prime()  
#     while q == p:               
#         q = generate_large_prime()
#     n = p * q
#     phi = (p - 1) * (q - 1)
#     e = random.randrange(2, phi)
#     while mod_inverse(e, phi) is None:
#         e = random.randrange(2, phi)
#     d = mod_inverse(e, phi)
#     return ((e, n), (d, n))

# # Encode
# def encodeRsa(data, key = public_key_server):
#     _code = json.dumps(data)
#     e, n = key
#     _encode = [pow(ord(char), e, n) for char in _code]
#     return _encode

# # Decode
# def decodeRsa(_encode):
#     d, n = PRIVATE_KEY
#     _decode = ''.join(chr(pow(char, d, n)) for char in _encode)
#     return json.loads(_decode)

def logout(tracker_conn):
    try:
        tracker_conn.sendall(json.dumps({'option': 'logout_request'}).encode())
        
        response = tracker_conn.recv(4096).decode()
        response_data = json.loads(response)
        
        if response_data['status'] == 'logout_accepted':
            tracker_conn.sendall(json.dumps({'option': 'logout_confirm'}).encode())
            print("[LOGOUT] Successfully logged out.")
        else:
            print("[LOGOUT] Tracker did not accept logout request.")
            
    except Exception as e:
        print("[ERROR] Logout error:", e)
    finally:
        tracker_conn.close()
        print("[DISCONNECTED] Client connection closed.")

def auth(tracker_conn):
    while True:
        command = input("Input command (signup/login/exit):")
        if command == "signup":
            email = input("Input your email: ")
            password = input("Input your password: ")
            print("Signing up...")
            status = signup(tracker_conn, email, password)
            if status:
                print("Sign up successful. Connected to tracker.")
                # No break; continue to the main command loop
                break
            else:
                print("Existed email")
                continue
        elif command == "login":
            # email = input("Input your email: ")
            # password = input("Input your password: ")
            email = "myemail"
            password = "mypassword"
            status = login(tracker_conn, email, password)
            if status:
                print("[LOGIN] Login successful")
                # No break; continue to the main command loop
                break
            else:
                print("[LOGIN] Login failed")
                continue
        elif command == "exit":
            os._exit(0)

if __name__ == "__main__":
    while True:
        tracker_conn = None
        while not tracker_conn:
            tracker_conn = connect_to_tracker()
        auth(tracker_conn)

        # Main command loop after successful login/signup
        server_thread = threading.Thread(target=server_main)
        server_thread.start()
        online = True
        while online:
            command = input("Input command (download/ping/publish/logout/exit):")
            if command == "download":
                file_name = input("Input file name to download: ")
                download(tracker_conn, file_name)
            elif command == "ping":
                user_input = input("Enter command in format 'ping <ip> <port>': ")
                parts = user_input.split()
                if len(parts) == 3 and parts[0].lower() == "ping":
                    try:
                        ip, port = parts[1], int(parts[2])  
                        ping(ip, port)  
                    except ValueError:
                        print("Invalid port. Please enter a valid integer for port.")
                else:
                    print("Invalid input. Please enter in format 'ping <ip> <port>'.")
            elif command == "publish":
                publish(tracker_conn)
            elif command == "logout":
                online = False
                logout(tracker_conn)
            elif command == "exit":
                online = False
                logout(tracker_conn)
                os._exit(0)
