import cv2
import mediapipe as mp

class Camera:
    def __init__(self, width=1280, height=720):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.mp_draw = mp.solutions.drawing_utils

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None, None, None
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_results = self.hands.process(rgb_frame)
        face_results = self.face_mesh.process(rgb_frame)
        
        return frame, hand_results, face_results

    def draw_landmarks(self, frame, hand_results, face_results=None):
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        # Optional: Draw face mesh (can be cluttered, maybe just eyes?)
        # if face_results and face_results.multi_face_landmarks:
        #     for face_landmarks in face_results.multi_face_landmarks:
        #         self.mp_draw.draw_landmarks(
        #             frame,
        #             face_landmarks,
        #             self.mp_face_mesh.FACEMESH_TESSELATION,
        #             landmark_drawing_spec=None,
        #             connection_drawing_spec=self.mp_draw.DrawingSpec(color=(128,128,128), thickness=1, circle_radius=1)
        #         )
                
        return frame

    def release(self):
        self.cap.release()
