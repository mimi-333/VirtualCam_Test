import io
import json
import numpy
import myType


class Gesture:
    def __init__(self, pathlist, name=""):
        self.name = name
        self.landmark_models = self.loadGesture(pathlist)

    def loadGesture(self, pathlist):
        gesture_list = []
        for path in pathlist:
            if path[-6] == "R":
                handedness = "Right"
            elif path[-6] == "L":
                handedness = "Left"
            else:
                print("error: direction cannot be read")
                exit()
            with open(path, "r") as fp:
                gesture_list.append(
                    myType.GESTURE(json.load(fp), handedness, 9))
        return gesture_list

    def matchPatterns(self, hand_data):
        for hand in hand_data:
            landmark_vector = self.normalizedLandmarks(hand.landmarks)
            for model in self.landmark_models:
                if model.handedness == hand.handedness:
                    score = numpy.arange(20, dtype=numpy.float64)
                    for idx, landmark in enumerate(landmark_vector):
                        if idx == 0:
                            continue
                        X = numpy.array(
                            [landmark[0], landmark[1], landmark[2]])
                        Y = numpy.array(
                            [model.landmarks[idx][0], model.landmarks[idx][1], model.landmarks[idx][2]])
                        score[idx-1] = numpy.dot(X, Y) / \
                            (numpy.linalg.norm(X) * numpy.linalg.norm(Y))
                    if 0.8 < numpy.mean(score):
                        results = (True,
                                   (hand.landmarks[model.base_index].x,
                                    hand.landmarks[model.base_index].y),
                                   self.name,
                                   model.handedness)
                        return results
            return (False,)

    def isMatch(self, results):
        return results[0]

    def calcCoodinates(self, results):
        return results[1]

    def normalizedLandmarks(self, landmarks):
        b_x = landmarks[0].x
        b_y = landmarks[0].y
        b_z = landmarks[0].z
        vector = [[0, 0, 0] for i in range(21)]

        for idx in range(1, 21):
            if idx % 4 == 1:
                x = landmarks[idx].x - b_x
                y = landmarks[idx].y - b_y
                z = landmarks[idx].z - b_z
                vector[idx] = [x, y, z]
            else:
                x = landmarks[idx].x - landmarks[idx-1].x
                y = landmarks[idx].y - landmarks[idx-1].y
                z = landmarks[idx].z - landmarks[idx-1].z
                vector[idx] = [x, y, z]

        return vector
