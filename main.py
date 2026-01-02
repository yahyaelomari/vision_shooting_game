from src.camera import Camera
from src.game_engine import GameEngine
from src.shapes import create_random_object, Particle
from src.gestures import GestureRecognizer, WinkRecognizer
from src.collision import check_collision
from src.ui import UIManager
from src.score_manager import ScoreManager
from src.gaze import GazeTracker
import random
import time
import pygame

def main():
    # Initialize Camera
    camera = Camera()
    
    # Initialize Game Engine
    game = GameEngine()
    
    # Initialize Gesture Recognizer
    # recognizer = GestureRecognizer() # Deprecated for shooting
    wink_recognizer = WinkRecognizer()
    
    # Initialize Gaze Tracker
    gaze_tracker = GazeTracker(1280, 720)
    
    # Initialize UI
    ui = UIManager(1280, 720)
    
    # Initialize Score Manager
    score_manager = ScoreManager()
    
    shapes = []
    particles = []
    score = 0
    player_name = "Player" # Default name
    last_spawn_time = 0
    spawn_interval = 2.0 # Seconds
    
    game_start_time = 0
    game_duration = 120 # 2 minutes
    
    running = True
    while running:
        # Get frame and landmarks
        frame, hand_results, face_results = camera.get_frame()
        if frame is None:
            break
            
        # Draw landmarks on frame (for debug/visuals)
        frame = camera.draw_landmarks(frame, hand_results, face_results)
        
        # Get aim position (Hand Tracking - Index Finger)
        aim_pos = None
        if hand_results.multi_hand_landmarks:
            tip = hand_results.multi_hand_landmarks[0].landmark[8]
            aim_pos = (int(tip.x * 1280), int(tip.y * 720))
            
        # Optional: Gaze/Face fallback or debug
        # if not aim_pos and face_results.multi_face_landmarks:
        #     aim_pos = gaze_tracker.get_gaze_point(face_results.multi_face_landmarks[0])

        # Handle Global Events (Pause, Input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if ui.state == "NAME_INPUT":
                name = ui.input_box.handle_event(event)
                if name is not None: # Enter pressed
                    player_name = name if name else "Anonymous"
                    ui.state = "GAME"
                    score = 0
                    shapes = []
                    particles = []
                    game_start_time = time.time()
                    last_spawn_time = time.time()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if ui.state == "GAME": ui.state = "PAUSED"
                    elif ui.state == "PAUSED": ui.state = "GAME"
                if event.key == pygame.K_SPACE:
                    if ui.state == "PAUSED": ui.state = "GAME"
                    elif ui.state == "GAME_OVER": ui.state = "MENU"
        
        if ui.state == "MENU":
            # Draw menu
            action = ui.draw_menu(game.screen, aim_pos)
            if action == "NAME_INPUT":
                # State change handled in draw_menu, just need to ensure loop continues
                pass
            elif action == "LEADERBOARD":
                ui.state = "LEADERBOARD"
            elif action == "EXIT":
                running = False
                
            # Update display for menu
            pygame.display.flip()
            game.clock.tick(30)
            
        elif ui.state == "NAME_INPUT":
            ui.draw_name_input(game.screen)
            pygame.display.flip()
            game.clock.tick(30)
            
        elif ui.state == "LEADERBOARD":
            high_scores = score_manager.get_high_scores()
            action = ui.draw_leaderboard(game.screen, high_scores, aim_pos)
            if action == "MENU":
                ui.state = "MENU"
            pygame.display.flip()
            game.clock.tick(30)
            
        elif ui.state == "PAUSED":
            ui.draw_pause_menu(game.screen, aim_pos)
            pygame.display.flip()
            game.clock.tick(30)
            
        elif ui.state == "GAME":
            # Check timer
            time_left = game_duration - (time.time() - game_start_time)
            if time_left <= 0:
                ui.state = "GAME_OVER"
                score_manager.add_score(player_name, score)
            
            # Detect gesture (Wink)
            shot_detected = False
            shot_pos = None
            
            is_winking = False
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    if wink_recognizer.detect_wink(face_landmarks):
                        is_winking = True
                        break
            
            if is_winking:
                shot_detected = True
                # Aim at current aim position
                if aim_pos:
                    shot_pos = aim_pos
                    
                    # Check collision
                    hit_shape = check_collision(shot_pos, shapes)
                    if hit_shape:
                        score += hit_shape.score
                        # Spawn particles
                        for _ in range(10):
                            particles.append(Particle(hit_shape.x, hit_shape.y, hit_shape.color))
                        shapes.remove(hit_shape)
                    else:
                        # MISS = GAME OVER
                        ui.state = "GAME_OVER"
                        score_manager.add_score(player_name, score)
            
            # Spawn shapes
            current_time = time.time()
            if current_time - last_spawn_time > spawn_interval:
                shapes.append(create_random_object(1280, 720))
                last_spawn_time = current_time
                spawn_interval = max(0.5, spawn_interval * 0.99) # Increase difficulty
                
            # Update shapes
            for s in shapes: s.update()
            shapes = [s for s in shapes if not s.is_expired()]
            
            # Update particles
            for p in particles: p.update()
            particles = [p for p in particles if p.is_alive()]
            
            # Update Game Engine
            # We pass aim_pos as 'crosshair_pos' for the persistent crosshair
            running = game.update(frame, hand_results, shapes=shapes, particles=particles, 
                                  shot_pos=shot_pos, score=score, 
                                  ui_manager=ui, time_left=time_left, hand_pos=aim_pos)
            
        elif ui.state == "GAME_OVER":
            high_scores = score_manager.get_high_scores()
            ui.draw_game_over(game.screen, score, high_scores, aim_pos)
            pygame.display.flip()
            game.clock.tick(30)
        
    camera.release()
    game.quit()

if __name__ == "__main__":
    main()
