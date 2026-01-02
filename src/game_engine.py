import pygame
import cv2
import numpy as np

class GameEngine:
    def __init__(self, width=1280, height=720, title="Hand Gesture Shooting Game"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

    def update(self, frame, results, **kwargs):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        # Convert OpenCV frame (BGR) to PyGame surface (RGB)
        # Frame is already RGB from camera.get_frame() if we used cvtColor there.
        # Let's check camera.py. It converts to RGB for MediaPipe but returns the original frame?
        # Re-reading camera.py: 
        # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # results = self.hands.process(rgb_frame)
        # return frame, results
        # So frame is BGR. We need to convert it for PyGame.
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
        frame_surface = pygame.transform.flip(frame_surface, True, False) # Pygame coords are different
        
        # Correct rotation and flipping for PyGame
        # OpenCV image is (Height, Width, Channels)
        # PyGame surfarray expects (Width, Height, Channels)
        frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
        
        # Blit camera feed
        self.screen.blit(frame_surface, (0, 0))
        
        # Draw shapes
        if 'shapes' in kwargs:
            for shape in kwargs['shapes']:
                shape.draw(self.screen)
                
        # Draw particles
        if 'particles' in kwargs:
            for p in kwargs['particles']:
                p.draw(self.screen)
        
        # Draw shot feedback (optional, maybe just particles now?)
        # Keeping it for immediate feedback
        if 'shot_pos' in kwargs and kwargs['shot_pos']:
            pos = kwargs['shot_pos']
            pygame.draw.circle(self.screen, (255, 255, 255), pos, 10)
            pygame.draw.line(self.screen, (255, 0, 0), (pos[0]-20, pos[1]), (pos[0]+20, pos[1]), 2)
            pygame.draw.line(self.screen, (255, 0, 0), (pos[0], pos[1]-20), (pos[0], pos[1]+20), 2)
        
        # Draw UI/Overlay via UIManager
        if 'ui_manager' in kwargs:
            ui = kwargs['ui_manager']
            score = kwargs.get('score', 0)
            time_left = kwargs.get('time_left', 0)
            hand_pos = kwargs.get('hand_pos', None)
            ui.draw_game_hud(self.screen, score, time_left, hand_pos)
        else:
            # Fallback
            score = kwargs.get('score', 0)
            self.draw_ui(score)
        
        pygame.display.flip()
        self.clock.tick(30)
        
        return True

    def draw_ui(self, score=0):
        fps = int(self.clock.get_fps())
        fps_text = self.font.render(f"FPS: {fps}", True, (0, 255, 0))
        self.screen.blit(fps_text, (10, 10))
        
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 0))
        self.screen.blit(score_text, (10, 40))

    def quit(self):
        pygame.quit()
