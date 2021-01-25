import face_recognition as fn
import os
import cv2
import numpy as np

from facerecognition.database import Database

class FaceRecognizer:

    def __init__(self, path=os.path.join(os.getcwd(), 'facerecognition', 'known_faces')):
        self.video_capture = cv2.VideoCapture(0)
        self._path = path
        self._db = Database(self._path)
        self._frame = None
        self._scale = 0.25

    def _update(self):
        ret, frame = self.video_capture.read()
        self._frame = frame
        small_frame = cv2.resize(frame, (0, 0), fx=self._scale, fy=self._scale)
        self._small_frame = small_frame[:, :, ::-1]  # BGR TO RGB
        self._face_locations = fn.face_locations(self._small_frame)
        self._face_encodings = fn.face_encodings(self._small_frame, self._face_locations)
        self._matches = self._recognize_faces()

    def _mark_faces(self, frame):
        face_locations = self._face_locations
        for (top, right, bottom, left), match in zip(face_locations, self._matches):
            top *= int(1 / self._scale)
            right *= int(1 / self._scale)
            bottom *= int(1 / self._scale)
            left *= int(1 / self._scale)
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            if match is not None:
                name = match.identity
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        return frame

    def get_frame(self, mark_faces=True):
        """
        Zwraca aktualną klatkę z kamery.
        Ze względu na długość przetwarzania obrazu ilość klatek na sekundę może się wahać między 1-2.
        Przetwarzanie obrazu jest wykonywane w osobnym procesie, dlatego wywołanie tej motody
        zwróci klatkę od razu
        :param mark_faces: czy zaznaczyć na klatcę wykryte twarze i ich osobowości
        :return: np.array reprezentujący aktualną klatkę (w formacie wykorzystywanym przez OpenCV)
        """
        frame = np.copy(self._frame)
        if mark_faces:
            frame = self._mark_faces(frame)
        return frame

    def _recognize_faces(self):
        encodings = self._face_encodings
        matches = []
        for encoding in encodings:
            match = self._db.get_match(encoding)
            matches.append(match)
        return matches

    def get_recognized_faces(self):
        """
        Zwraca listę ostatnio wykrytych osób (może być ich wiele w jednej klatce)
        :return: liste krotek (imie, twarz odczytaną z bazy danych) dla wykrytych osób. ("Nieznana twarz", None) dla nierozpoznanych
        """
        pass