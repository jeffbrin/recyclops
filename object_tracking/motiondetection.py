import cv2
import numpy as np
import os
import time 

def sort_images(filenames):
    def remove_letters(string: str):
        final = str()
        for c in string:
            if c.isnumeric():
                final += c
        return int(final)
    return sorted(filenames, key=remove_letters)

motion_threshold = 0.02
images = sort_images([os.path.join('testphotos', image) for image in os.listdir('testphotos')])
prev_frame = cv2.imread(images[0])
prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

for image in images[1:]:
    filepath = image

    img = cv2.imread(filepath)

    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    window_name = 'image'
    # cv2.imshow(window_name, img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    frame_diff = cv2.absdiff(gray, prev_frame)
    _, thresh = cv2.threshold(frame_diff, 40, 255, cv2.THRESH_BINARY)
    prev_frame = gray.copy()

    motion_pixels = np.count_nonzero(thresh)
    total_pixels = thresh.size
    motion_ratio = motion_pixels / total_pixels

    cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(window_name, thresh)
    
    if motion_ratio >= motion_threshold:
        cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
        cv2.imshow(window_name, thresh)

    time.sleep(0.05)

