# import zmq

# context = zmq.Context()
# socket = context.socket(zmq.REP)
# socket.bind("tcp://127.0.0.1:5555")

# picam2 = Picamera2()
# config = picam2.create_preview_configuration({"size": (1920,1080)})
# picam2.configure(config)
# picam2.set_controls({"ExposureTime": 50000, "AnalogueGain": 2.0})
# picam2.start()

# while True:
#     message = socket.recv()
#     data = io.BytesIO()
#     picam2.capture_file(data, format='jpeg')
#     socket.send(data.getvalue())

#!/usr/bin/python3

import time

from picamera2 import Picamera2, Preview

i = 0
FrameRate = 2.7
frame_time = 1000000 // FrameRate 


picam2 = Picamera2()
# picam2.start_preview(Preview.QTGL)

capture_config = picam2.create_still_configuration(main={"format": 'RGB888', "size": (1000, 1000)})
picam2.configure(capture_config)

# picam2.set_controls({"FrameDurationLimits":(frame_time, frame_time)})
# picam2.start(show_preview=True)
start = time.time()
picam2.start()
for i in range(10):
    picam2.capture_file(f"test{i}.jpg")

print(f"10 images taken in {round(time.time()-start, 2)} seconds")