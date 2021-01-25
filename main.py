from facerecognition.facerecognizer import FaceRecognizer
import cv2
import numpy as np
import os

def main():
    fr = FaceRecognizer()

    while True:
        fr._update()
        frame = fr.get_frame(mark_faces=True)

        cv2.imshow('Video', frame)
        cv2.imwrite(os.path.join(os.path.curdir, "frame.jpg"), frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
