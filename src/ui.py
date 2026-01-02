import pygame
import math
import time

class NeonButton:
    def __init__(self, x, y, width, height, text, color=(0, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (255, 255, 255)
        self.glow_radius = 15
        self.font = pygame.font.SysFont("Arial", 32, bold=True)
        
        self.hover_start_time = 0
        self.hover_threshold = 1.5
        self.is_hovered = False

    def draw(self, screen, hand_pos=None):
        # Check hover
        self.is_hovered = False
        if hand_pos and self.rect.collidepoint(hand_pos):
            self.is_hovered = True
            if self.hover_start_time == 0:
                self.hover_start_time = time.time()
        else:
            self.hover_start_time = 0
            
        # Draw Glow
        if self.is_hovered:
            for i in range(3):
                pygame.draw.rect(screen, (*self.color, 50 - i*10), 
                                 self.rect.inflate(self.glow_radius + i*5, self.glow_radius + i*5), 
                                 border_radius=10)
        
        # Draw Button Body
        pygame.draw.rect(screen, (20, 20, 20), self.rect, border_radius=10)
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=10)
        
        # Draw Text
        text_surf = self.font.render(self.text, True, self.color if not self.is_hovered else self.hover_color)
        screen.blit(text_surf, (self.rect.centerx - text_surf.get_width()//2, self.rect.centery - text_surf.get_height()//2))
        
        # Draw Progress
        if self.is_hovered:
            progress = (time.time() - self.hover_start_time) / self.hover_threshold
            if progress >= 1.0:
                return True
            
            # Draw progress bar at bottom
            pygame.draw.rect(screen, self.color, (self.rect.x + 5, self.rect.bottom - 10, (self.rect.width - 10) * progress, 5))
            
        return False

class Crosshair:
    def __init__(self):
        self.color = (255, 255, 0) # Yellow
        self.size = 20
        self.angle = 0
        
    def draw(self, screen, pos):
        if not pos:
            return
            
        x, y = pos
        self.angle = (self.angle + 5) % 360
        
        # Rotating outer ring
        # Draw 4 segments
        for i in range(4):
            start_angle = math.radians(self.angle + i * 90)
            end_angle = math.radians(self.angle + i * 90 + 60)
            pygame.draw.arc(screen, self.color, (x - self.size, y - self.size, self.size*2, self.size*2), start_angle, end_angle, 2)
            
        # Inner dot
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 3)
        
        # Cross lines
        pygame.draw.line(screen, self.color, (x - 10, y), (x + 10, y), 1)
        pygame.draw.line(screen, self.color, (x, y - 10), (x, y + 10), 1)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        self.state = "MENU"
        
        # Neon Buttons
        # Neon Buttons
        self.start_btn = NeonButton(width//2 - 100, height//2 - 90, 200, 60, "START", (0, 255, 0))
        self.leaderboard_btn = NeonButton(width//2 - 100, height//2 - 10, 200, 60, "SCORES", (0, 255, 255))
        self.exit_btn = NeonButton(width//2 - 100, height//2 + 70, 200, 60, "EXIT", (255, 0, 0))
        
        self.back_btn = NeonButton(width//2 - 100, height - 100, 200, 60, "BACK", (255, 0, 0))
        
        self.crosshair = Crosshair()
        
        # Input Box
        self.input_box = InputBox(width//2 - 100, height//2, 140, 32)

    def draw_menu(self, screen, hand_pos=None):
        # Dark overlay with grid pattern (simulated)
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Title with Glow
        title_text = "CYBER SHOOTER"
        title_surf = self.font_large.render(title_text, True, (0, 255, 255))
        # Simple glow shadow
        title_shadow = self.font_large.render(title_text, True, (0, 100, 100))
        screen.blit(title_shadow, (self.width//2 - title_surf.get_width()//2 + 2, 100 + 2))
        screen.blit(title_surf, (self.width//2 - title_surf.get_width()//2, 100))
        
        # Buttons
        if self.start_btn.draw(screen, hand_pos):
            self.state = "NAME_INPUT" # Go to name input instead of GAME
            self.input_box.text = ""
            self.input_box.txt_surface = self.input_box.font.render("", True, self.input_box.color)
            self.input_box.active = True # Auto activate
            return "NAME_INPUT"
            
        if self.leaderboard_btn.draw(screen, hand_pos):
            return "LEADERBOARD"

        if self.exit_btn.draw(screen, hand_pos):
            return "EXIT"
            
        # Draw Crosshair
        self.crosshair.draw(screen, hand_pos)
                
        return None

    def draw_name_input(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("ENTER NAME", True, (0, 255, 255))
        screen.blit(text, (self.width//2 - text.get_width()//2, 100))
        
        self.input_box.update()
        self.input_box.draw(screen)
        
        hint = self.font_medium.render("Press ENTER to Start", True, (255, 255, 255))
        screen.blit(hint, (self.width//2 - hint.get_width()//2, self.height//2 + 50))

    def draw_game_hud(self, screen, score, time_left, hand_pos):
        # Draw Crosshair
        self.crosshair.draw(screen, hand_pos)
        
        # HUD Bar
        pygame.draw.rect(screen, (0, 0, 0, 150), (0, 0, self.width, 60))
        pygame.draw.line(screen, (0, 255, 255), (0, 60), (self.width, 60), 2)
        
        # Score
        score_text = self.font_medium.render(f"SCORE: {score}", True, (255, 255, 0))
        screen.blit(score_text, (20, 15))
        
        # Time
        color = (0, 255, 0) if time_left > 30 else (255, 0, 0)
        time_text = self.font_medium.render(f"TIME: {int(time_left)}", True, color)
        screen.blit(time_text, (self.width - 150, 15))

        # Draw Crosshair
        self.crosshair.draw(screen, hand_pos)
        
    def draw_pause_menu(self, screen, hand_pos=None):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("PAUSED", True, (255, 255, 0))
        screen.blit(text, (self.width//2 - text.get_width()//2, 100))
        
        # Resume Button (simulated for now, or just text instruction)
        resume_text = self.font_medium.render("Press SPACE to Resume", True, (255, 255, 255))
        screen.blit(resume_text, (self.width//2 - resume_text.get_width()//2, self.height//2))
        
        # Draw Crosshair
        self.crosshair.draw(screen, hand_pos)

    def draw_game_over(self, screen, score, high_scores, hand_pos=None):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (self.width//2 - text.get_width()//2, 50))
        
        score_text = self.font_medium.render(f"YOUR SCORE: {score}", True, (255, 255, 255))
        screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 130))
        
        # Leaderboard
        y_offset = 200
        lb_title = self.font_medium.render("HIGH SCORES", True, (0, 255, 255))
        screen.blit(lb_title, (self.width//2 - lb_title.get_width()//2, y_offset))
        
        y_offset += 40
        for i, s in enumerate(high_scores):
            color = (255, 215, 0) if i == 0 else (200, 200, 200) # Gold for 1st
            s_text = self.font_medium.render(f"{i+1}. {s}", True, color)
            screen.blit(s_text, (self.width//2 - s_text.get_width()//2, y_offset))
            y_offset += 35
            
        restart_text = self.font_medium.render("Press SPACE to Menu", True, (0, 255, 0))
        screen.blit(restart_text, (self.width//2 - restart_text.get_width()//2, self.height - 80))
        
        # Draw Crosshair
        self.crosshair.draw(screen, hand_pos)

    def draw_leaderboard(self, screen, high_scores, hand_pos=None):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        text = self.font_large.render("LEADERBOARD", True, (0, 255, 255))
        screen.blit(text, (self.width//2 - text.get_width()//2, 50))
        
        y_offset = 150
        for i, s in enumerate(high_scores):
            color = (255, 215, 0) if i == 0 else (200, 200, 200) # Gold for 1st
            # Handle both dict and old int format just in case, though ScoreManager handles loading
            name = s.get('name', 'Anonymous')
            score = s.get('score', 0)
            
            s_text = self.font_medium.render(f"{i+1}. {name}: {score}", True, color)
            screen.blit(s_text, (self.width//2 - s_text.get_width()//2, y_offset))
            y_offset += 50
            
        if self.back_btn.draw(screen, hand_pos):
            return "MENU"
            
        # Draw Crosshair
        self.crosshair.draw(screen, hand_pos)
        return None
