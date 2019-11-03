import audio_model
import alert_system
import record
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

def status_operations(status, model):
    
    while (status == "normal"):
        # *not implementing yet* Get overlapping recordings - 2 second overlap
        recording = np.asarray([record.record_sample()])
        prediction = model.predict(recording)[0][0]
        if prediction == 1:
            status = "recording"
            break
        else:
            print("No Clap")

    if status == "recording":
        print("Gunshot detected.")
        print("Sending alerts...")
        alert_system.send_alert("West Wing,Room 1C13")
        print("Current Status: Recording (Please wait...)")
        seconds = 10
        fs = 90000
        myrecording = sd.rec(int(seconds* fs), samplerate = fs, channels=2)
        sd.wait()
        write("test.wav", fs, myrecording)
        myrecording = sd.playrec(myrecording, samplerate = fs, channels=2)
        print("Playing last ", seconds, " seconds of audio...")
        user_update_status = input("Enter 1234 to confirm valid threat or enter anything else to clear alarm (false detection): ")
        if (user_update_status != "1234"):
            print("Alarm successfully cleared. Resuming normal status...")
            status = "normal"
            alert_system.send_false_alarm()
            status_operations(status, model)
        else:
            print("Sending alerts...")
            alert_system.send_alert_confirmation("West Wing,Room 1C13")
            print("Alert police...")
            print("Continue recording...")
        


if __name__ == "__main__":

    status = "normal" # initialize to normal operation (no emergency)
    model = audio_model.build_model()

    status_operations(status, model)