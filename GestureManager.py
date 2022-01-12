import Gesture
import MultiGesture
import os


class GestureManager:
    def __init__(self):
        self.gesture_list = []  # Gesture.Gesture()
        self.loadGestures()

    def loadGestures(self):
        root_path = "./Gestures"
        dir_list = os.listdir(root_path)
        for dir_path in dir_list:
            if os.path.isdir(os.path.join(root_path, dir_path)):
                file_list = []
                for file_path in os.listdir(os.path.join(root_path, dir_path)):
                    if file_path[-5:] == ".json":
                        file_list.append(os.path.join(
                            root_path, dir_path, file_path))
                if dir_path[-2:] != "_M":
                    gesture = Gesture.Gesture(file_list, dir_path)
                else:
                    gesture = MultiGesture.MultiGesture(file_list, dir_path)
                self.gesture_list.append(gesture)

    def matchGestures(self, hand_data):
        result = ()
        for gesture in self.gesture_list:
            result = gesture.matchPatterns(hand_data)
            if result[0] == True:
                return result
        return result
