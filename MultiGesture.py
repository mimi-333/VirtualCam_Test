import Gesture
import numpy


class MultiGesture(Gesture.Gesture):
    def __init__(self, pathlist, name=""):
        self.name = name
        self.gestures = self.loadGesture(pathlist)
        for gesture in self.gestures:
            gesture.changeIndex(2)

    def matchPatterns(self, hands):
        results = ()
        count = 0
        for model in self.gestures:
            for hand in hands:
                if model.handedness == hand.handedness:
                    landmark_vector = self.normalizedLandmarks(hand.landmarks)
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
                        result = (True,
                                  (hand.landmarks[model.base_index].x,
                                   hand.landmarks[model.base_index].y),
                                  self.name,
                                  model.handedness)
                        count += 1
                        results += result
                    else:
                        return (False,)
        if len(self.gestures) != count:
            return (False,)
        return results
