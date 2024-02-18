import socket
import wave, pyaudio, pickle, struct

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9611

def upload_stream(wav_data):

    CHUNK = 1024 # Byte Chunnk size
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        socket_address = (host_ip, port-1)
        print(f"Server should be listening at {socket_address}")
        
        client_socket.connect(socket_address)
        print(f"Connected to {socket_address}")
        print(f"Wave data: {wav_data}")
        
        client_socket.sendall(wav_data)
    except Exception as e:
        print(f"[-] Exception: {e}")
    
    client_socket.close()

upload_stream(None)
