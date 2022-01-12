class HAND:
    landmarks : list
    handedness : str

    def __init__(self, landmarks, handedness):
        self.landmarks = landmarks
        self.handedness = handedness

class HANDs:
    hands : list

    def __init__(self, model = None):
        self.hands = []
        if model != None:
            self.convertLandmarks(model)
        else:
            "HANDs error"

    def convertLandmarks(self, model):
        if model.multi_hand_landmarks:
            for idx in range(len(model.multi_hand_landmarks)):
                handedness = model.multi_handedness[idx].classification[0].label
                self.hands.append(HAND(model.multi_hand_landmarks[idx].landmark,handedness))
                
class GESTURE(HAND):
    base : tuple

    def __init__(self, landmarks, handedness, base_index = 0):
        self.landmarks = landmarks
        self.handedness = handedness
        self.base_index = base_index

    def changeIndex(self, index):
        self.base_index = index