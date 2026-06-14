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
                    elif event.key == pygame.K_RETURN:
                        self.check_puzzle_answer()
                    else:
                        if len(self.user_input_text) < 5:
                            self.user_input_text += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_submit_rect.collidepoint(event.pos):
                        self.check_puzzle_answer()

            elif self.state == STATE_FEEDBACK:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    if self.feedback_message == "Correct!":
                        self.state = STATE_MENU
                        self.dialogue_index = 0
                        self.user_input_text = ""
                    else:
                        self.state = STATE_PUZZLE

    def check_puzzle_answer(self):
        if self.user_input_text.strip() == self.correct_answer:
            self.feedback_message = "Correct!"
            self.feedback_color = COLOR_CORRECT
        else:
            self.feedback_message = "Incorrect! Try again."
            self.feedback_color = COLOR_INCORRECT
        self.state = STATE_FEEDBACK

    # --- UPDATE LOGIC ---
    def update(self):
        pass 

    # --- DRAWING METHODS ---
    def draw(self):
        self.screen.fill(COLOR_BG)

        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state == STATE_DIALOGUE:
            self.draw_dialogue()
        elif self.state == STATE_PUZZLE:
            self.draw_puzzle()
        elif self.state == STATE_FEEDBACK:
            self.draw_feedback()

        pygame.display.flip()

    def draw_menu(self):
        title_surf = self.font_title.render("PYTHON DETECTIVE", True, COLOR_PRIMARY)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_surf, title_rect)

        subtitle_surf = self.font_body.render("Cozy Mystery Programming Adventure", True, COLOR_TEXT_DARK)
        subtitle_rect = subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
        self.screen.blit(subtitle_surf, subtitle_rect)

        self.btn_start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40, 240, 50)
        pygame.draw.rect(self.screen, COLOR_ACCENT, self.btn_start_rect, border_radius=8)

        btn_text = self.font_body.render("Start Investigation", True, COLOR_TEXT_LIGHT)
        btn_text_rect = btn_text.get_rect(center=self.btn_start_rect.center)
        self.screen.blit(btn_text, btn_text_rect)

    def draw_dialogue(self):
        pygame.draw.rect(self.screen, (220, 230, 235), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        portrait_rect = pygame.Rect(80, 100, 180, 260)
        pygame.draw.rect(self.screen, COLOR_ACCENT, portrait_rect, border_radius=12)
        p_label = self.font_body.render("[Mayor Portrait]", True, COLOR_TEXT_LIGHT)
        self.screen.blit(p_label, p_label.get_rect(center=portrait_rect.center))

        dialogue_box = pygame.Rect(40, 380, SCREEN_WIDTH - 80, 130)
        surf_panel = pygame.Surface((dialogue_box.width, dialogue_box.height), pygame.SRCALPHA)
        surf_panel.fill(COLOR_PANEL)
        self.screen.blit(surf_panel, (dialogue_box.x, dialogue_box.y))
        pygame.draw.rect(self.screen, COLOR_PRIMARY, dialogue_box, width=3, border_radius=10)

        speaker, text = self.dialogue_lines[self.dialogue_index]

        speaker_surf = self.font_body.render(speaker, True, COLOR_ACCENT)
        self.screen.blit(speaker_surf, (dialogue_box.x + 20, dialogue_box.y + 15))

        text_surf = self.font_body.render(text, True, COLOR_TEXT_DARK)
        self.screen.blit(text_surf, (dialogue_box.x + 20, dialogue_box.y + 55))

        hint_surf = self.font_body.render("Press SPACE or Tap to continue...", True, (130, 140, 150))
        self.screen.blit(hint_surf, (dialogue_box.right - 260, dialogue_box.bottom - 30))

    def draw_puzzle(self):
        header_surf = self.font_body.render("CASE FILE #1: The Broken Printing String", True, COLOR_PRIMARY)
        self.screen.blit(header_surf, (40, 30))

        editor_rect = pygame.Rect(40, 80, SCREEN_WIDTH - 80, 240)
        pygame.draw.rect(self.screen, (34, 40, 49), editor_rect, border_radius=8)

        lines = self.puzzle_prompt.split('\n')
        for idx, line in enumerate(lines):
            line_surf = self.font_code.render(line, True, (142, 227, 182) if "#" in line else COLOR_TEXT_LIGHT)
            self.screen.blit(line_surf, (60, 110 + (idx * 35)))

        input_box_rect = pygame.Rect(390, 142, 60, 32)
        pygame.draw.rect(self.screen, COLOR_TEXT_DARK, input_box_rect, border_radius=4)
        pygame.draw.rect(self.screen, COLOR_ACCENT if self.input_active else COLOR_PRIMARY, input_box_rect, width=2, border_radius=4)

        input_surf = self.font_code.render(self.user_input_text, True, COLOR_ACCENT)
        self.screen.blit(input_surf, (input_box_rect.x + 10, input_box_rect.y + 2))

        hint_surf = self.font_body.render(self.puzzle_hint, True, COLOR_TEXT_DARK)
        self.screen.blit(hint_surf, (40, 340))

        self.btn_submit_rect = pygame.Rect(SCREEN_WIDTH - 220, 420, 180, 50)
        pygame.draw.rect(self.screen, COLOR_PRIMARY, self.btn_submit_rect, border_radius=8)
        submit_text = self.font_body.render("Submit Patch", True, COLOR_TEXT_LIGHT)
        self.screen.blit(submit_text, submit_text.get_rect(center=self.btn_submit_rect.center))

    def draw_feedback(self):
        modal_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 200)
        pygame.draw.rect(self.screen, COLOR_BG, modal_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.feedback_color, modal_rect, width=4, border_radius=12)

        msg_surf = self.font_title.render(self.feedback_message, True, self.feedback_color)
        msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(msg_surf, msg_rect)

        sub_text = "Tap / Space to continue" if self.feedback_message == "Correct!" else "Tap / Space to try again"
        sub_surf = self.font_body.render(sub_text, True, COLOR_TEXT_DARK)
        sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(sub_surf, sub_rect)


if __name__ == "__main__":
    game = PythonDetectiveGame()
    game.run()
