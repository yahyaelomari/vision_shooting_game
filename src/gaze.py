import math
import numpy as np

class GazeTracker:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Landmark indices for Left Eye
        # Corners
        self.LEFT_EYE_RIGHT_CORNER = 362 
        self.LEFT_EYE_LEFT_CORNER = 263
        # Iris Center (Refined landmarks)
        self.LEFT_IRIS_CENTER = 468
        
        # Landmark indices for Right Eye
        self.RIGHT_EYE_RIGHT_CORNER = 33
        self.RIGHT_EYE_LEFT_CORNER = 133
        self.RIGHT_IRIS_CENTER = 473
        
        # Smoothing
        self.prev_x, self.prev_y = width // 2, height // 2
        self.alpha = 0.2 # Smoothing factor (lower = smoother but more lag)
        
        # Calibration / Sensitivity
        # These ranges define the "normal" movement of the iris within the eye
        # Normalized ratio: 0.0 (left) to 1.0 (right)
        # We map a sub-range (e.g., 0.3 to 0.7) to the full screen to make it easier
        self.x_min = 0.35
        self.x_max = 0.65
        self.y_min = 0.35
        self.y_max = 0.60 # Eyes don't move down as much usually

    def get_gaze_point(self, face_landmarks):
        if not face_landmarks:
            return None
            
        landmarks = face_landmarks.landmark
        
        # Calculate for Left Eye
        left_ratio_x, left_ratio_y = self._get_eye_ratio(landmarks, 
                                                         self.LEFT_EYE_RIGHT_CORNER, 
                                                         self.LEFT_EYE_LEFT_CORNER, 
                                                         self.LEFT_IRIS_CENTER)
                                                         
        # Calculate for Right Eye
        right_ratio_x, right_ratio_y = self._get_eye_ratio(landmarks, 
                                                           self.RIGHT_EYE_RIGHT_CORNER, 
                                                           self.RIGHT_EYE_LEFT_CORNER, 
                                                           self.RIGHT_IRIS_CENTER)
        
        # Average the ratios
        avg_ratio_x = (left_ratio_x + right_ratio_x) / 2.0
        avg_ratio_y = (left_ratio_y + right_ratio_y) / 2.0
        
        # Map to screen coordinates
        # Normalize based on sensitivity range
        norm_x = (avg_ratio_x - self.x_min) / (self.x_max - self.x_min)
        norm_y = (avg_ratio_y - self.y_min) / (self.y_max - self.y_min)
        
        # Clamp to 0-1
        norm_x = max(0.0, min(1.0, norm_x))
        norm_y = max(0.0, min(1.0, norm_y))
        
        # Scale to screen
        # Note: Camera is mirrored, so we might need to invert X if not already handled
        # Usually gaze ratio logic: 
        # If iris is closer to left corner (screen left), ratio is low.
        # If iris is closer to right corner (screen right), ratio is high.
        # Let's verify direction.
        
        target_x = int(norm_x * self.width)
        target_y = int(norm_y * self.height)
        
        # Smoothing
        self.prev_x = int(self.prev_x * (1 - self.alpha) + target_x * self.alpha)
        self.prev_y = int(self.prev_y * (1 - self.alpha) + target_y * self.alpha)
        
        return (self.prev_x, self.prev_y)

    def _get_eye_ratio(self, landmarks, inner_idx, outer_idx, iris_idx):
        # Inner/Outer corner landmarks
        inner = landmarks[inner_idx]
        outer = landmarks[outer_idx]
        iris = landmarks[iris_idx]
        
        # Total eye width
        eye_width = math.sqrt((outer.x - inner.x)**2 + (outer.y - inner.y)**2)
        if eye_width == 0: return 0.5, 0.5
        
        # Distance from inner corner to iris
        # Project iris onto the line connecting corners for horizontal ratio
        # Vector Inner->Outer
        vec_eye = np.array([outer.x - inner.x, outer.y - inner.y])
        # Vector Inner->Iris
        vec_iris = np.array([iris.x - inner.x, iris.y - inner.y])
        
        # Projection length
        proj = np.dot(vec_iris, vec_eye) / np.linalg.norm(vec_eye)
        
        ratio_x = proj / eye_width
        
        # Vertical ratio is harder with just corners. 
        # Simple approximation: Relative Y position of iris compared to corners
        # But eyes are curved. 
        # Better: Use eyelids. But for simplicity, let's try direct Y relative to eye center Y.
        eye_center_y = (inner.y + outer.y) / 2.0
        # Normalize by some height factor (e.g. 1/4 of width)
        # If iris.y < center.y (up), value is negative.
        # We want 0 (up) to 1 (down).
        # Let's assume a range of +/- 0.02 in Y coordinate space relative to width
        
        # Alternative: Use eyelids landmarks if available.
        # Top eyelid: 159 (Right), 386 (Left)
        # Bottom eyelid: 145 (Right), 374 (Left)
        # Let's stick to a simpler heuristic first or use the eyelids if we know indices.
        # Left Eye Top/Bottom: 386 / 374
        # Right Eye Top/Bottom: 159 / 145
        
        if inner_idx == 362: # Left Eye
            top = landmarks[386]
            bottom = landmarks[374]
        else: # Right Eye
            top = landmarks[159]
            bottom = landmarks[145]
            
        eye_height = math.sqrt((top.x - bottom.x)**2 + (top.y - bottom.y)**2)
        if eye_height == 0: return ratio_x, 0.5
        
        # Distance from top to iris
        dist_top = math.sqrt((iris.x - top.x)**2 + (iris.y - top.y)**2)
        ratio_y = dist_top / eye_height
        
        return ratio_x, ratio_y
