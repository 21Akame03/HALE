import openwakeword
from openwakeword.model import Model
import os
import pyaudio
import numpy as np 
import time

# One time download of all models required
# openwakeword.utils.download_models()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1280

audio = pyaudio.PyAudio()
mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

model = Model(wakeword_models=["../Stella.tflite", "../staella.tflite", "../hey_staella.tflite"], inference_framework="tflite", vad_threshold=0.5)

def listen_hotword():
    while True:
        audio = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)
        prediction = model.predict(audio)

        for mdl in model.prediction_buffer.keys():
            scores = list(model.prediction_buffer[mdl])
            print(scores[len(scores)-1])
            if scores.pop() > 0.05:
                print("Stella")
                return True
            
            scores = [] 


listen_hotword()

