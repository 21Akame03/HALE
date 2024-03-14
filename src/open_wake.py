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

model = Model(wakeword_models=["../haeli.onnx", "../Stella.onnx"], inference_framework="onnx", vad_threshold=0.4)




if __name__ == "__main__":
    print("Listerning for Wake words (HAELI)")

    while True:
        audio = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)

        prediction = model.predict(audio)

        # Column titles
        n_spaces = 16
        output_string_header = """
            Model Name         | Score | Wakeword Status
            --------------------------------------
            """
        for mdl in model.prediction_buffer.keys():
                # Add scores in formatted table
                scores = list(model.prediction_buffer[mdl])
                curr_score = format(scores[-1], '.20f').replace("-", "")

                output_string_header += f"""{mdl}{" "*(n_spaces - len(mdl))}   | {curr_score[0:5]} | {"--"+" "*20 if scores[-1] <= 0.5 else "Wakeword Detected!"}
                """

         # Print results table
        print(output_string_header, "                             ", end='\r')
