import PIL.Image
import cv2
import numpy as np
import os
import time 
from time import sleep
import PIL

def motion_detection(image_filepath: str, previous_image_filepath: str, mask_dim: list[list, list] =  [[[0, 500], [0, 500]]], take_image_funct = lambda: None) -> int:
    """
    Returns the index of the mask where motion was detected.
    Returns -1 if no motion was detected.
    """

    for i, mask in enumerate(mask_dim):
        motion_threshold = 0.02
        prev_frame = cv2.imread(previous_image_filepath)
        prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        prev_frame = masking(prev_frame, mask)


        filepath = image_filepath

        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        gray = masking(gray, mask)

        frame_diff = cv2.absdiff(gray, prev_frame)
        _, thresh = cv2.threshold(frame_diff, 40, 255, cv2.THRESH_BINARY)

        motion_pixels = np.count_nonzero(thresh)
        total_pixels = (mask[0][1] - mask[0][0]) * (mask[1][1] - mask[1][0])
        motion_ratio = motion_pixels / total_pixels

        if motion_ratio >= motion_threshold:

            sleep(0.15)
            filename = take_image_funct()
            img = cv2.imread(filename)
            img = masking(img, mask)

            print("MOVEMENT")
            # TODO: Remove
            cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('window', thresh)
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            cv2.imwrite("masked_item.jpg", masking(img, mask))
            return i, "masked_item.jpg"
    return -1, None

def masking(image, mask : list[list, list]):

    zeros_mask = np.zeros(image.shape[:2], np.uint8)
    cv2.rectangle(zeros_mask, [mask[0][0], mask[1][0]], [mask[0][1], mask[1][1]], 255, -1)

    masked = cv2.bitwise_and(image, image, mask = zeros_mask)

    return masked

# masking('object_tracking/test0.jpg', [[0, 90], [290, 450]])