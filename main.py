import pygame
import sys

# Initialize Pygame
pygame.init()

# --- CONSTANTS & CONFIG ---
# Target 16:9 Aspect Ratio (Mobile friendly landscape)
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60

# Cozy Pastel Color Palette
COLOR_BG = (245, 240, 230)       # Warm ivory
COLOR_PRIMARY = (74, 96, 122)     # Cozy slate blue
COLOR_ACCENT = (222, 133, 101)    # Soft terracotta
COLOR_TEXT_DARK = (44, 53, 64)    # Charcoal
COLOR_TEXT_LIGHT = (255, 255, 255)
COLOR_PANEL = (255, 255, 255, 230) # Semi-transparent white
COLOR_CORRECT = (92, 144, 116)   # Sage green
COLOR_INCORRECT = (204, 91, 91)   # Muted red

# Game States
STATE_MENU = "MAIN_MENU"
STATE_DIALOGUE = "DIALOGUE_SCENE"
STATE_PUZZLE = "PUZZLE_SCENE"
STATE_FEEDBACK = "FEEDBACK_SCENE"

class PythonDetectiveGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Python Detective")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_MENU

        # Fonts - Fixed for Android/Cross-platform Compatibility
        self.font_title = pygame.font.SysFont(None, 48, bold=True)
        self.font_body = pygame.font.SysFont(None, 24)
        self.font_code = pygame.font.SysFont(None, 26, bold=True)

        # Game State Variables
        self.dialogue_index = 0
        self.user_input_text = ""
        self.input_active = True
        self.feedback_message = ""
        self.feedback_color = COLOR_CORRECT

        # Phase 1 Script Data
        self.dialogue_lines = [
            ("Mayor Pip", "Thank goodness you're here, Detective! The town clock has stopped completely!"),
            ("Mayor Pip", "I tried to look at the automated control script, but it has a strange error."),
            ("Mayor Pip", "Can you look at this print statement for me? It's missing something vital.")
        ]

        # Puzzle Definition
        self.puzzle_prompt = "# Fix the bug to print out the activation code:\nprint('System Active' _ "
        self.puzzle_hint = "Hint: How do you close a string function call?"
        self.correct_answer = ")"

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    # --- EVENT HANDLING ---
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_start_rect.collidepoint(event.pos):
                        self.state = STATE_DIALOGUE

            elif self.state == STATE_DIALOGUE:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.dialogue_index += 1
                    if self.dialogue_index >= len(self.dialogue_lines):
                        self.state = STATE_PUZZLE

            elif self.state == STATE_PUZZLE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_input_text = self.user_input_text[:-1]
                    elif event.key

