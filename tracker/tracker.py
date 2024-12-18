import socket
import threading
import mysql.connector as mysql
import json
import os, sys
import random
import time
from datetime import datetime
from tkinter import Tk, messagebox
sys.path.append(os.path.abspath("../gui"))
from admin import GUITRACKER
from lstadmin import GUILISTADMIN

S_TERMINAL = None
S_LIVING = None

TRACKER_PORT = 50000
TRACKER_ADDRESS = "127.0.0.1" 

connection_to_db = mysql.connect(host="localhost", user="root", password="", database="computer_network")
cursor=connection_to_db.cursor()
# cursor.execute("Some query"")

living_conn = []
public_keys = []
public_key, private_key = None, None

def gettime():
    now = datetime.now()
    return str(now.strftime("%H:%M:%S"))

def view_peers():
    # print("=== Current Active Peers ===")
    # if not living_conn:
    #     print("No active peers.")
    #     return
    # for index, conn in enumerate(living_conn, start=1):
    #     ip, port = conn.getpeername()
    #     print(f"{index}. IP: {ip}, Port: {port}")
    # print(f"Total active peers: {len(living_conn)}")
    cursor.execute("SELECT DISTINCT IP, port, hostname FROM peers;")
    result = cursor.fetchall()
    for idx, (IP, port, hostname) in enumerate(result, start=1):
        print(f"ID:{idx} | IP:{IP} | Port:{port} | Hostname:{hostname}")
    return result

def ping(ip, port, window, entry, request_count=5):
    if not ip:
        window.after(0, lambda: messagebox.showinfo("Lỗi", "Vui lòng nhập IP"))
        return
    if not port:
        window.after(0, lambda: messagebox.showinfo("Lỗi", "Vui lòng nhập Port"))
        return
    for i in range(request_count):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((ip, port))
            message = {
                'option': 'ping',
                'message':f"ping | ICMP_order: {i + 1}"
            }
            entry.insert('end', f"[{gettime()}] => Gửi yêu cầu {i + 1} đến {ip}:{port}   \n")
            entry.see("end")

            client_socket.sendall(json.dumps(message).encode())
            client_socket.settimeout(2)
            tmp = client_socket.recv(4096).decode()
            response = json.loads(tmp)
            mess = response['message']
            entry.insert('end', f"[{gettime()}] => Nhận phản hồi {i + 1}: {mess} từ {ip}:{port} \n")
            entry.see("end")
        except socket.timeout:
            entry.insert('end', f"[{gettime()}] => Hết thời gian yêu cầu \n")
            entry.see("end")
        except Exception as error:
            entry.insert('end', f"[{gettime()}] => Lỗi gửi yêu cầu {i + 1} đến {ip}:{port}: {error} \n")
            entry.see("end")
        finally:
            client_socket.close()  
        time.sleep(1) 
    window.after(0, lambda: messagebox.showinfo("Hoàn tất", "Đã kết thúc ping!"))

def response_publish(conn):
    conn.sendall(json.dumps({"status": True}).encode())
    
def client_handler(conn, addr):
    # global public_key
    # conn.sendall(json.dumps({"public_key": public_key}).encode())
    # print(f"[INFO] Sent public key to client at {addr}")
    # login(conn, addr)
    # print("[LOGIN] Logined, listening...")
    while True:
        req = conn.recv(8192).decode()
        if not req:
            continue
        
        # Determine request
        request = json.loads(req)
        print(request)
        req_option = request['option']
        ip = addr[0]
        port = request['port'] if 'port' in request else ""
        hostname = request['hostname'] if 'hostname' in request else ""
        file_name = request['file_name'] if 'file_name' in request else ""
        file_size = request['file_size'] if 'file_size' in request else ""
        piece_hash = request['piece_hash'] if 'piece_hash' in request else ""
        piece_size = request['piece_size'] if 'piece_size' in request else ""
        piece_order = request['piece_order'] if 'piece_order' in request else ""
        match req_option:
            case "login":
                email = request['email']
                password = request['password']
                login(conn, email, password, port)

            case "signup":
                email = request['email']
                password = request['password']
                signup(conn,  email, password)

            case "download":
                num_order_in_file_str = ','.join(map(str, piece_order))
                piece_hash_str = ','.join(map(str, piece_hash))
                print(str(num_order_in_file_str))
                print(str(piece_hash_str))
                # Execute the query
                cursor.execute("""
                    SELECT * FROM peers 
                    WHERE file_name = %s 
                    AND hostname NOT IN (%s)
                    AND piece_order NOT IN (%s) 
                    AND piece_hash NOT IN (%s)
                    ORDER BY piece_order ASC;
                """, (file_name, hostname, num_order_in_file_str, piece_hash_str))
                result = cursor.fetchall()
                print(f"SELECT * FROM peers WHERE file_name = {file_name} AND piece_order NOT IN ({num_order_in_file_str}) AND piece_hash NOT IN ({piece_hash_str}) ORDER BY piece_order ASC;")
                print(result)
                if result:
                    metainfo = []
                    for ID, IP, port, hostname, file_name, file_size, piece_hash, piece_size, piece_order in result:
                        tmp = {
                            'ID': ID,
                            'IP': IP,
                            'port': port,
                            'hostname': hostname,
                            'file_name': file_name,
                            'file_size': file_size,
                            'piece_hash': piece_hash,
                            'piece_size': piece_size,
                            'piece_order': piece_order
                        }
                        metainfo.append(tmp)
                    # conn.sendall(json.dumps({'metainfo': metainfo}).encode())
                    data_to_send = json.dumps({'metainfo': metainfo}).encode()
                    conn.sendall(len(data_to_send).to_bytes(4, 'big'))
                    for i in range(0, len(data_to_send), 4096):
                        conn.sendall(data_to_send[i:i+4096])
                else :
                    conn.sendall(json.dumps({'metainfo': []}).encode())   
            case "publish":
                print("[PUBLISH] Publish start successful")
                delete_query = """
                    DELETE FROM peers
                    WHERE hostname = %s AND file_name = %s AND piece_order = %s; 
                """
                cursor.execute(delete_query, (hostname, file_name, piece_order))
                connection_to_db.commit()
                insert_query = """
                    INSERT INTO peers (ip, port, hostname, file_name, file_size, piece_hash, piece_size, piece_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (ip, port, hostname, file_name, file_size, piece_hash, piece_size, piece_order))
                connection_to_db.commit()
                response_publish(conn)
                print(ip, port, hostname, file_name, file_size, piece_hash, piece_size, piece_order)
                print("[PUBLISH] Publish successful")

            case "view_peers":
                data = view_peers()
                conn.sendall(json.dumps(data).encode())

            case "logout_request":
                conn.sendall(json.dumps({'status': 'logout_accepted'}).encode())

            case "logout_confirm":
                if conn in living_conn:
                    living_conn.remove(conn)
                    print(f"[LOGOUT] {addr} has logged out.")
                    print("[CONNECTION] Living connection: ", len(living_conn))
                    if S_LIVING:
                        S_LIVING.delete(0, 'end')
                        S_LIVING.insert(0, str(len(living_conn)))
                    try:
                        S_TERMINAL.insert('end', f"[{gettime()}] => {addr} đã đăng xuất \n")
                        S_TERMINAL.see("end")
                    except:
                        pass
                conn.close()
                break
            
            case "ping":
                mes = request['message']
                try:
                    S_TERMINAL.insert('end', f"[{gettime()}] => Nhận yêu cầu ping từ {addr[0]} \n")
                    S_TERMINAL.see("end")
                except:
                    pass
                icmp_order = mes.split(":")[-1].strip()
                response_message = {
                    'option': 'pong',
                    'message': f"pong | ICMP_order: {icmp_order}"
                }
                conn.sendall(json.dumps(response_message).encode())
                conn.close()
                break

def login(conn, email, password, client_port):
    try:
        while True:
            if not email:
                conn.sendall(json.dumps({'status': False, 'mes': '[LOGIN] Missing email'}).encode())
                return False
            elif not email:
                conn.sendall(json.dumps({'status': False, 'mes': '[LOGIN] Missing password'}).encode())
                return False
            else :
                cursor.execute("SELECT email FROM login WHERE email = %s AND password = %s;", (email, password))
                successfull = cursor.fetchall() 
                print(successfull)
                if successfull:
                    peer_info = {'status': True, 'hostname': email}
                    conn.sendall(json.dumps(peer_info).encode())
                    if conn not in living_conn:
                        living_conn.append(conn)
                    # print(conn)
                    print("[CONNECTION] Living connection: ", len(living_conn))
                    if S_LIVING:
                        S_LIVING.delete(0, 'end')
                        S_LIVING.insert(0, str(len(living_conn)))
                    IP, port = conn.getpeername()
                    hostname = peer_info['hostname']
                    # Assuming conn is your socket object

                    print("Client IP:", IP)
                    print("Client Port:", port)
                    try:
                        S_TERMINAL.insert('end', f"[{gettime()}] => Đăng nhập mới từ {IP}:{port} \n")
                        S_TERMINAL.see("end")
                    except:
                        pass
                    cursor.execute("""
                        UPDATE peers
                        SET IP = %s, port = %s
                        WHERE hostname = %s;
                    """, (IP, client_port, hostname))
                    connection_to_db.commit()
                    return True
                else :
                    conn.sendall(json.dumps({'status': False}).encode())
                    return False
    except Exception as error:
        print("[ERROR] Function login error", error)
    finally:
        # erase info of this conn in table peers before close connection
        print("[LOGIN] Function login run ok")

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
# def encodeRsa(data):
#     _code = data['code']
#     public_key = data['key']
#     e, n = public_key
#     _encode = [pow(ord(char), e, n) for char in _code]
#     return _encode

# # Decode
# def decodeRsa(data):
#     _encode = data['code']
#     private_key = data['key']
#     d, n = private_key
#     _decode = ''.join(chr(pow(char, d, n)) for char in _encode)
#     return _decode

def signup(conn,  email, password):
    try:
        # Kiểm tra xem email đã tồn tại trong database chưa
        cursor.execute("SELECT * FROM login WHERE email = %s;", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.sendall(json.dumps({'status': False, 'mes': 'Email already exists'}).encode())
        else:
            # Thêm người dùng mới vào database
            cursor.execute("INSERT INTO login (email, password) VALUES (%s, %s);", (email, password))
            connection_to_db.commit()
            conn.sendall(json.dumps({'status': True, 'mes': 'Sign up successful'}).encode())
            print(f"[SIGNUP] New user created: {email}")
            try:
                S_TERMINAL.insert('end', f"[{gettime()}] => {email} đã tạo tài khoản \n")
                S_TERMINAL.see("end")
            except:
                pass
    except Exception as error:
        print("[ERROR] Function signup error:", error)
        # conn.sendall(json.dumps({'status': False, 'mes': 'Signup failed'}).encode())
    finally:
        print("[TEST] Function signup run ok")

# def terminal():
#     option = input()
#     while option != "exit":
#         if option == "ping":
#             user_input = input("Enter command in format 'ping <ip> <port>': ")
#             parts = user_input.split()
#             if len(parts) == 3 and parts[0].lower() == "ping":
#                 try:
#                     ip, port = parts[1], int(parts[2])  
#                     ping(ip, port)  
#                 except ValueError:
#                     print("Invalid port. Please enter a valid integer for port.")
#             else:
#                 print("Invalid input. Please enter in format 'ping <ip> <port>'.")
#         elif option == "view_peers":
#             view_peers()
#         option = input()
#     os._exit(0)

def server_main():
    # global public_key, private_key
    # public_key, private_key = generate_keypair()
    # print("[INFO] Public Key:", public_key)
    # print("[INFO] Private Key:", private_key)
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP/IP
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Config: can reuse IP immediately after closed
        server_socket.bind((TRACKER_ADDRESS, TRACKER_PORT))
        server_socket.listen()
        print(f"[LISTENING] Server is listening on PORT = {TRACKER_PORT}")
    except:
        print("KHÔNG KHỞI ĐỘNG ĐƯỢC TRACKER")
        os._exit(0)
        

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"[ACCEPT] Connected to clients throught {conn.getsockname()}")
            print(f"[ACCEPT] Client socket: {addr}")
            # data = conn.recv(4096).decode()
            # if data.startswith("ping"):
            #     thread = threading.Thread(target=ping_handler, args=(conn, addr, data))
            # else:
            #     thread = threading.Thread(target=client_handler, args=(conn, addr, data))
            thread = threading.Thread(target=client_handler, args=(conn, addr))
            thread.start()
            print(f"[SERVER] Active connections: {threading.active_count() - 1}")
            # print("[TEST] Finding bug")

    except Exception as error:
            print(error)
    finally:
        server_socket.close()
        cursor.close()

def openListPeer(window):
    res = view_peers()
    # if not res:
    #     window.after(0, lambda: messagebox.showinfo("Lỗi", "Không lấy được danh sách peer!"))
    #     return
    GUILISTADMIN(res, "DANH SÁCH CÁC PEER")

def saveterminal(entry):
    global S_TERMINAL
    S_TERMINAL = entry

def saveliving(entry):
    global S_LIVING
    S_LIVING = entry


if __name__ == "__main__":
    server_thread = threading.Thread(target=server_main)
    server_thread.start()

    GUITRACKER(TRACKER_ADDRESS, TRACKER_PORT, ping, openListPeer, saveterminal, saveliving)
    
    os._exit(0)
    server_thread.join()