import socketio 
import eventlet
import time 

# create Socketio server 
sio = socketio.Server(cors_allowed_origins="*", async_mode='eventlet')


def VAD_STATUS_emit(active):
    sio.emit('VAD_STATUS', {'active': active})
    print(f"Sent Active: {active}")

@sio.event
def connect(sid, environ, auth):
    print('connect', sid)

@sio.event
def disconnect(sid):
    print('disconnect', sid)

app = socketio.WSGIApp(sio)
eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 8000)), app)

