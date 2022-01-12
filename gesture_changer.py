import cv2
import mediapipe as mp
import io
import json

print("なんて名前にしますー？ -> ", end="")
filename = input()
print("おっけー")

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FPS, 30)           # カメラFPSを30FPSに設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # カメラ画像の縦幅を720に設定

with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:  # if ESC is pressed, save and exit
            # print(results.multi_hand_landmarks[0].landmark[0].x)
            direction = ""
            if results.multi_handedness[0].classification[0].label == "Right":
                direction = "R"
            else:
                direction = "L"

            with open(filename + "_" + direction + ".json", "w") as f:
                b_x, b_y, b_z = results.multi_hand_landmarks[0].landmark[0].x, \
                    results.multi_hand_landmarks[0].landmark[0].y, \
                    results.multi_hand_landmarks[0].landmark[0].z
                landmark_vector = [[0, 0, 0] for i in range(21)]
                for i in range(5):
                    idx = 4 * i + 1
                    x = results.multi_hand_landmarks[0].landmark[idx].x - b_x
                    y = results.multi_hand_landmarks[0].landmark[idx].y - b_y
                    z = results.multi_hand_landmarks[0].landmark[idx].z - b_z
                    landmark_vector[idx] = [x, y, z]
                for i in range(5):
                    for j in range(2, 5):
                        idx = 4 * i + j
                        x = results.multi_hand_landmarks[0].landmark[idx].x - \
                            results.multi_hand_landmarks[0].landmark[idx-1].x
                        y = results.multi_hand_landmarks[0].landmark[idx].y - \
                            results.multi_hand_landmarks[0].landmark[idx-1].y
                        z = results.multi_hand_landmarks[0].landmark[idx].z - \
                            results.multi_hand_landmarks[0].landmark[idx-1].z
                        landmark_vector[idx] = [x, y, z]
                json.dump(landmark_vector, f)
            break
        # if cv2.waitKey(5) & 0xFF == 27:  # if ESC is pressed, exit
        #  break
cap.release()
