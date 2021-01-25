
class RecognizedFace:

    def __init__(self, identity, frame_location):
        self.identity = identity #string
        self.frame_location = frame_location #lokalizacja na klatce ((left_top_x, left_top_y), (bottom_right_x, botton_right_y))