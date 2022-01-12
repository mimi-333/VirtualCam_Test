import cv2
import mediapipe as mp
import myType
import GestureManager as GM
import LayerManager as LM
import Rectangle
import Image

gManager = GM.GestureManager()
lManager = LM.LayerManager()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

pict_img = cv2.imread("SpaceCat.png", -1)

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
            hand = myType.HANDs(results)
            result = gManager.matchGestures(hand.hands)
            if result[0] == True:
                if result[2] == "square1_M":
                    # if result[2] == "square1_M" or result[2] == "square2_M":
                    obj = lManager.getSelectedObj()
                    if obj == None:
                        obj = Rectangle.Rectangle((result[1], result[5]))
                        lManager.register(obj)
                    else:
                        obj.expand((result[1], result[5]))
                        lManager.updateObj(obj)
                elif result[2] == "square2_M":
                    obj = lManager.getSelectedObj()
                    if obj == None:
                        obj = Image.Image((result[1], result[5]), pict_img)
                        lManager.register(obj)
                    else:
                        obj.expand((result[1], result[5]))
                        lManager.updateObj(obj)
                elif result[2] == "grab":
                    obj = lManager.getSelectedObj()
                    if obj == None:
                        obj = lManager.checkHit(result[1])
                    if obj != None:
                        obj.move(result[1])
                elif result[2] == "choki":
                    obj = lManager.checkHit(result[1])
                    lManager.delete(obj)
                else:
                    lManager.cancelSelection()
            """for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand = type_Hand.HAND(results.multi_hand_landmarks[idx].landmark, results.multi_handedness[idx].classification[0].label)
                result = gManager.matchGestures(hand)
                judge = "False"
                if result[0] == True:
                    judge = result[2]
                cv2.putText(image, judge, (500, 40 * (idx + 1)),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255))"""
        lManager.draw(image)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:  # if ESC is pressed, exit
            break
cap.release()
