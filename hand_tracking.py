# hand_tracking.py
import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1, detection_conf=0.7):
        self.hands_module = mp.solutions.hands
        self.hands = self.hands_module.Hands(max_num_hands=max_hands, min_detection_confidence=detection_conf)
        self.mp_draw = mp.solutions.drawing_utils

    def get_index_finger_tip(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Index finger tip is landmark 8
                index_finger = hand_landmarks.landmark[8]
                h, w, _ = frame.shape
                x, y = int(index_finger.x * w), int(index_finger.y * h)
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.hands_module.HAND_CONNECTIONS)
                return x, y
        return None
