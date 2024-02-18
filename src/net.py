import socket, os
import threading, wave, pyaudio, pickle, struct


hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)


print(f'Host ip: {host_ip}')
port = 9611

def audio_stream():

    p = pyaudio.PyAudio()
    CHUNK = 1024 # Chunks in which data will be broken into
    
    # open a pyaudio stream 
    stream = p.open(format=p.get_format_from_width(2),
                    rate=16000,
                    channels=1,
                    output=True,
                    frames_per_buffer=CHUNK)

    # Create Socket to send the stream (Circuit streaming)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_address = (host_ip, port-1)
    print(f'Attempting to connect to Server at ${socket_address}')
    
    client_socket.connect(socket_address)
    print(f"Connected tp ${socket_address}")
    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024) # creating packets of 4Kb
                if not packet: break 

                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            stream.write(frame)

        except:
            break

    client_socket.close()
    print("Audio Closed")
    
t1 = threading.Thread(target=audio_stream, args=())
t1.start()
