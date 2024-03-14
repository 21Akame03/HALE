import VAD
from halo import Halo
import time, logging
import os
from open_wake_word import listen_hotword
import network_func

def main():
    # Start audio with VAD
    vad_audio = VAD.VADAudio(aggressiveness= 3,
                         device=None,
                         input_rate=16000,
                         file=None)
    print("Listening (ctrl-C to exit)...")
    frames = vad_audio.vad_collector()
    
    network_func.VAD_STATUS_emit(True)
    
    # Wake word detection using open wake word 
    detected = listen_hotword()


    # Wake word detection using picovoice Porcupine model
    spinner = None
    
    spinner = Halo(spinner='line')
    wav_data = bytearray()
    for frame in frames:
        if frame is not None and detected:
            if spinner: spinner.start()
            wav_data.extend(frame)
        else:
            if spinner: spinner.stop()
            logging.debug("end utterence")

            # Put byte array into wav file 
            vad_audio.write_wav(os.path.join("../", "spch_text.wav"), wav_data)
            

if __name__ == "__main__":
    main()
