import os
import pickle
import face_recognition
import logging

def _get_subregion(image, region):
    x1, y1, x2, y2 = region
    return image[y1:y2, x1:x2, :]

class DatabasePerson:

    def __init__(self, main_folder):
        self._folder = main_folder
        self._load()

    def _load_from_files(self):
        for file in os.listdir(self._folder):
            if not os.path.isfile(os.path.join(self._folder, file)) or file.lower().endswith("pickle"):
                continue
            logging.info("Processing", self._folder, file)
            filepath = os.path.join(self._folder, file)
            image = self._load_image(filepath)
            encoding, face_location, face = self._load_encoding(filepath, image)
            self._images.append((image, encoding, face_location, face))

    def _load_encoding(self, filepath, image):
        filename = "".join(os.path.basename(filepath).split('.')[:-1])
        pickle_file = os.path.join(self._folder, "{}.pickle".format(filename))
        face_location = None
        encoding = None
        face = None
        if not os.path.exists(pickle_file):
            logging.debug(pickle_file, "does not exist!")
            face_location = face_recognition.face_locations(image)[0] #possible error
            encoding = face_recognition.face_encodings(image, [face_location])[0] #possible error ??
            face = _get_subregion(image, face_location)
            with open(pickle_file, "wb+") as f:
                pickle.dump({'face_location':face_location, 'encoding':encoding, 'face':face}, f)
        else:
            logging.debug("Opening", pickle_file)
            with open(pickle_file, "rb") as f:
                data = pickle.load(f)
                face_location = data['face_location']
                encoding = data['encoding']
                face = data['face']
        return encoding, face_location, face

    def _load_image(self, path):
        image = None
        try:
            image = face_recognition.load_image_file(path)
        except FileNotFoundError:
            logging.error("Could not find file", path)

        return image


    def _load(self):
        self._identity = " ".join((x.title() for x in os.path.basename(os.path.normpath(self._folder)).split('_')))
        self._images = []
        self._load_from_files()

    @property
    def identity(self):
        """
        Zwraca imie i nazwisko danej osoby.
        :return: str
        """
        return self._identity

    @property
    def encodings(self):
        return [encoding for _, encoding, _, _ in self._images]

    def is_match(self, face_encoding):
        """
        Czy ta face_encoding pasuje do tej osoby
        :param face_encoding: enkodowany obszar do porównania
        :return: Jeśli pasuje: zwraca twa
        """
        encodings = self.encodings
        results = face_recognition.compare_faces(encodings, face_encoding)
        for i, v in enumerate(results):
            if v: #match
                return self._images[i][3]
        return None

    def get_distance(self, encoding):
        """
        Zwraca najmniejszy dystans do zakodowanej twarzy
        :param encoding: zakodowana twarz
        :return:
        """
        return min([face_recognition.face_distance([encoding], my_encoding)[0] for _, my_encoding, _, _ in self._images])

class Database:

    def __init__(self, path):
        self._path = path
        self._load_database()

    def _load_database(self):
        self._database = []
        for directory in os.listdir(self._path):
            directory = os.path.join(self._path, directory)
            if os.path.isdir(directory):
                self._database.append(DatabasePerson(directory))

    def get_match(self, face_encoding, tolerance=0.6):
        """
        Zwraca listę instancji DatabasePerson pasujących do face_encoding
        :param face_encoding: enkodowana twarz
        :return: lista DatabasePerson
        """
        matches = [(p.get_distance(face_encoding), p) for p in self._database]
        mini = None
        for d, p in matches:
            if mini is None or mini[0] > d:
                mini = (d, p)
        if mini is not None:
            if mini[0] <= tolerance:
                return mini[1]
        return None