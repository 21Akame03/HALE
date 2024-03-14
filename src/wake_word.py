import os
import struct 
import wave
from datetime import datetime

import pvporcupine
from pvrecorder import PvRecorder


class pico_wake:
    def __init__(self):
        self.access_key = "hY2Zk1JT9VPFqbh1qGLFtsQ+ujVfXfs2U6aTpm9NoZJKVoxdwUrBcQ=="
             
        try:
            self.porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keywords=["jarvis"],
                    keyword_paths=[os.path.join("..", "hale_linux.ppn")]
                    )
        
        except Exception as e:
            print(f"[-] Error: {e}")
        
        cur_device = 1
        print(f"device_index: {cur_device}")
        self.recorder = PvRecorder(
                frame_length=self.porcupine.frame_length,
                device_index=cur_device
                )

    def detect_wake_word(self):
        self.recorder.start()
            
        try:
            while True:
                pcm = self.recorder.read()
                result = self.porcupine.process(pcm)

                if result >= 0:
                    print("Detected")
        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            self.recorder.delete()
            self.porcupine.delete()

