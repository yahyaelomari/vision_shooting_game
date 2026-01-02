import math

class GestureRecognizer:
    def __init__(self):
        self.prev_index_tip = None
        self.velocity_threshold = 20.0 # Pixels per frame, adjust as needed

    def is_shooting_gesture(self, hand_landmarks):
        # Shooting gesture: Index finger extended, others folded
        # Landmarks:
        # 0: Wrist
        # 5, 6, 7, 8: Index finger
        # 9, 10, 11, 12: Middle finger
        # 13, 14, 15, 16: Ring finger
        # 17, 18, 19, 20: Pinky
        # 1, 2, 3, 4: Thumb
        
        # Helper to check if finger is folded
        def is_finger_folded(tip_idx, pip_idx, wrist_idx=0):
            # Check distance to wrist or relative y position
            # Simple check: tip is below pip (in screen coords, y increases downwards)
            # But hand can be rotated.
            # Better: Check distance from tip to wrist vs pip to wrist.
            # If tip is closer to wrist than pip, it's folded.
            
            tip = hand_landmarks.landmark[tip_idx]
            pip = hand_landmarks.landmark[pip_idx]
            wrist = hand_landmarks.landmark[wrist_idx]
            
            d_tip = math.sqrt((tip.x - wrist.x)**2 + (tip.y - wrist.y)**2)
            d_pip = math.sqrt((pip.x - wrist.x)**2 + (pip.y - wrist.y)**2)
            
            return d_tip < d_pip

        # Index finger should be extended
        # Tip (8) should be further from wrist (0) than PIP (6)
        if is_finger_folded(8, 6):
            return False
            
        # Middle, Ring, Pinky should be folded
        if not is_finger_folded(12, 10):
            return False
        if not is_finger_folded(16, 14):
            return False
        if not is_finger_folded(20, 18):
            return False
            
        # Thumb: Optional, but usually folded or relaxed for "gun"
        # Let's ignore thumb for now to make it easier, or require it to be up?
        # User said "Index finger extended, other fingers folded".
        # Usually thumb is up for "gun" or folded for "pointing".
        # Let's assume "pointing" style or "gun" style.
        # If thumb is folded, it's more like pointing.
        # Let's stick to the core requirement: Index extended, others folded.
        
        return True

    def detect_shoot(self, hand_landmarks, width, height):
        if not self.is_shooting_gesture(hand_landmarks):
            self.prev_index_tip = None
            return False, None

        # Get index tip coordinates
        tip = hand_landmarks.landmark[8]
        x, y = int(tip.x * width), int(tip.y * height)
        
        # Check velocity
        if self.prev_index_tip is not None:
            dx = x - self.prev_index_tip[0]
            dy = y - self.prev_index_tip[1]
            dist = math.sqrt(dx*dx + dy*dy)
            
            # Update prev
            self.prev_index_tip = (x, y)
            
            # Check if velocity exceeds threshold
            # And maybe direction? "Quick forward movement".
            # "Forward" in 2D usually means towards the screen (z-axis) or up/down?
            # Or maybe just "movement".
            # User said "Quick forward movement".
            # In 2D camera, "forward" (towards camera) might mean hand getting bigger?
            # Or maybe they mean "in the direction of pointing".
            # Let's assume high velocity in any direction for now, or maybe Z-axis if available.
            # MediaPipe gives Z coordinate (relative to wrist).
            # But Z is not very reliable for velocity without depth camera.
            # Let's assume "forward" means "moving the hand quickly".
            
            if dist > self.velocity_threshold:
                return True, (x, y)
        else:
            self.prev_index_tip = (x, y)
            
        return False, (x, y)

class WinkRecognizer:
    def __init__(self):
        # Eye landmarks (MediaPipe Face Mesh)
        # Left Eye
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        # Right Eye
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        
        self.EAR_THRESHOLD = 0.22 # Below this, eye is closed
        self.consecutive_frames = 0
        self.WINK_FRAMES = 2 # Number of frames to confirm wink
        
    def calculate_ear(self, landmarks, indices):
        # EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
        # Vertical distances
        p2 = landmarks[indices[1]]
        p6 = landmarks[indices[5]]
        v1 = math.sqrt((p2.x - p6.x)**2 + (p2.y - p6.y)**2)
        
        p3 = landmarks[indices[2]]
        p5 = landmarks[indices[4]]
        v2 = math.sqrt((p3.x - p5.x)**2 + (p3.y - p5.y)**2)
        
        # Horizontal distance
        p1 = landmarks[indices[0]]
        p4 = landmarks[indices[3]]
        h = math.sqrt((p1.x - p4.x)**2 + (p1.y - p4.y)**2)
        
        if h == 0: return 0
        return (v1 + v2) / (2.0 * h)

    def detect_wink(self, face_landmarks):
        if not face_landmarks:
            return False
            
        landmarks = face_landmarks.landmark
        
        left_ear = self.calculate_ear(landmarks, self.LEFT_EYE)
        right_ear = self.calculate_ear(landmarks, self.RIGHT_EYE)
        
        # Wink logic: One eye closed, other open
        # Closed if EAR < THRESHOLD
        
        left_closed = left_ear < self.EAR_THRESHOLD
        right_closed = right_ear < self.EAR_THRESHOLD
        
        # XOR for wink (one closed, one open)
        is_winking = (left_closed and not right_closed) or (right_closed and not left_closed)
        
        # Optional: Blink detection (both closed) - ignore or treat as shot?
        # User asked for "winking".
        # Blinking (both eyes) might be natural blinking.
        # So strictly XOR is better to avoid accidental shots on blink.
        
        if is_winking:
            self.consecutive_frames += 1
        else:
            self.consecutive_frames = 0
            
        if self.consecutive_frames >= self.WINK_FRAMES:
            self.consecutive_frames = 0 # Reset to prevent rapid fire on hold
            return True
            
        return False
