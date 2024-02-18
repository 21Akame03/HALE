import VAD
from halo import Halo
import time, logging
import os
import upload

def main():
    # Start audio with VAD
    vad_audio = VAD.VADAudio(aggressiveness= 3,
                         device=None,
                         input_rate=16000,
                         file=None)
    print("Listening (ctrl-C to exit)...")
    frames = vad_audio.vad_collector()

    # Stream from microphone to DeepSpeech using VAD
    spinner = None
    
    spinner = Halo(spinner='line')
    wav_data = bytearray()
    for frame in frames:
        if frame is not None:
            if spinner: spinner.start()
            wav_data.extend(frame)
        else:
            if spinner: spinner.stop()
            logging.debug("end utterence")
            
            # send byte array straight to server
            upload.upload_stream(wav_data)

            # Put byte array into wav file 
            # vad_audio.write_wav(os.path.join("../", "spch_text.wav"), wav_data)
            wav_data = bytearray()

if __name__ == "__main__":
    main()
