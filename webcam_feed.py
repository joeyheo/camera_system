# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    webcam_feed.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: joeyheo <sheo2@ucsc.edu>                   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/08/16 15:51:15 by joeyheo           #+#    #+#              #
#    Updated: 2023/08/16 15:51:26 by joeyheo          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import cv2
import numpy as np

def add_watermark(frame, watermark_image_path):
    watermark = cv2.imread(watermark_image_path, cv2.IMREAD_UNCHANGED)
    (wH, wW) = watermark.shape[:2]

    # If the watermark image has a 4th channel, it's considered as an alpha channel which defines transparency
    if watermark.shape[2] == 4:
        (B, G, R, A) = cv2.split(watermark)
        B = cv2.bitwise_and(B, B, mask=A)
        G = cv2.bitwise_and(G, G, mask=A)
        R = cv2.bitwise_and(R, R, mask=A)
        watermark = cv2.merge([B, G, R])

    # Set the position of the watermark at the bottom-right corner
    (h, w) = frame.shape[:2]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    overlay = np.zeros((h, w, 4), dtype="uint8")
    overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark

    # Blend the two images together using transparent overlays
    cv2.addWeighted(overlay, 0.25, frame, 1.0, 0, frame)

    return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

def main():
    cap = cv2.VideoCapture(0)  # Open webcam: '0' usually refers to the default webcam

    if not cap.isOpened():
        print("Could not open webcam!")
        exit()

    while True:
        ret, frame = cap.read()  # Read a frame

        if not ret:
            break

        # Add watermark to the captured frame
        watermarked_frame = add_watermark(frame, "/path/to/your/watermark.png")

        # Display the watermarked frame
        cv2.imshow('Webcam Feed', watermarked_frame)

        # Close the window when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the webcam resource
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
