import socket
import sys
import threading

listening_port = 60000
max_connection = 50 
buffer_size = 10240 # 10 KB
tracker = '127.0.0.1'
trackerport = 60001

def proxy_server(conn, addr, data):
    try:
        print(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4 - TCP/IP
        sock.connect((tracker, trackerport))
        sock.sendall(data)

        while True:
            try:
                reply = sock.recv(buffer_size)
                if len(reply) > 0:
                    conn.sendall(reply)
                else:   
                    break
            except Exception as error:
                print(error)
                break
        sock.close()
        conn.close()
    except socket.error as error:
        print(error)
        sock.close()
        conn.close()
        sys.exit(1)
        
def start():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4 - TCP/IP
        sock.bind(('', listening_port))
        sock.listen(max_connection)
        print("[*] Proxy server started successfully [ %d ]" % (listening_port))
    except Exception as error:
        print(error)
        sys.exit()

    while True:
        try:
            sock.settimeout(2)
            conn, addr = sock.accept()
            data = conn.recv(buffer_size)
            thread = threading.Thread(target=proxy_server, args=(conn, addr, data))
            thread.start()
        except socket.timeout:
            pass
        except Exception as error:
            print(error)

if __name__ == "__main__":
    start()
