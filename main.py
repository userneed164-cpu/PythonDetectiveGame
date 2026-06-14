‎import pygame
‎import sys
‎import random
‎
‎# Initialize Pygame
‎pygame.init()
‎
‎# --- CONSTANTS & CONFIG ---
‎SCREEN_WIDTH = 960
‎SCREEN_HEIGHT = 540
‎FPS = 60
‎
‎# Cozy Pastel Color Palette
‎COLOR_BG = (245, 240, 230)       # Warm ivory
‎COLOR_PRIMARY = (74, 96, 122)     # Cozy slate blue
‎COLOR_ACCENT = (222, 133, 101)    # Soft terracotta
‎COLOR_TEXT_DARK = (44, 53, 64)    # Charcoal
‎COLOR_TEXT_LIGHT = (255, 255, 255)
‎COLOR_PANEL = (255, 255, 255, 230) # Semi-transparent white
‎COLOR_CORRECT = (92, 144, 116)   # Sage green
‎COLOR_INCORRECT = (204, 91, 91)   # Muted red
‎COLOR_EDITOR_BG = (34, 40, 49)    # Dark code editor bg
‎COLOR_CODE_GREEN = (142, 227, 182)
‎COLOR_CODE_BLUE = (97, 175, 239)  # For keywords
‎COLOR_CODE_YELLOW = (229, 192, 123) # For strings
‎
‎# Game States
‎STATE_MENU = "MAIN_MENU"
‎STATE_DIALOGUE = "DIALOGUE_SCENE"
‎STATE_PUZZLE = "PUZZLE_SCENE"
‎STATE_FEEDBACK = "FEEDBACK_SCENE"
‎STATE_GAME_OVER = "GAME_OVER_SCENE"
‎STATE_LEVEL_SELECT = "LEVEL_SELECT"
‎
‎# --- EXPANDED QUEST SYSTEM ---
‎QUESTS = [
‎    # --- BEGINNER LEVELS ---
‎    {
‎        "difficulty": "Beginner",
‎        "title": "The Clock Tower",
‎        "lines": [
‎            ("Mayor Pip", "Thank goodness you're here, Detective! The town clock has stopped completely!"),
‎            ("Mayor Pip", "I tried to look at the automated control script, but it has a strange error."),
‎            ("Mayor Pip", "Can you look at this print statement for me? It's missing something vital.")
‎        ],
‎        "prompt": "# Case 1: Fix the bug to print the activation code:\nprint('System Active' _ ",
‎        "hint": "Hint: How do you close a string function call?",
‎        "correct": ")",
‎        "input_offset_x": 390,
‎        "code_syntax_hint": "parenthesis"
‎    },
‎    {
‎        "difficulty": "Beginner",
‎        "title": "The Security Gate",
‎        "lines": [
‎            ("Chief Codey", "Detective! The security gate is locked and won't let anyone out!"),
‎            ("Chief Codey", "Someone altered the variable assignment script in the main terminal."),
‎            ("Chief Codey", "Look at how the status variable is being set. Something is broken.")
‎        ],
‎        "prompt": "# Case 2: Assign 'open' to the gate status variable:\ngate_status _ 'open'",
‎        "hint": "Hint: What operator do we use to assign a value in Python?",
‎        "correct": "=",
‎        "input_offset_x": 170,
‎        "code_syntax_hint": "operator"
‎    },
‎    {
‎        "difficulty": "Beginner",
‎        "title": "The Database Function",
‎        "lines": [
‎            ("Professor Py", "Ah, Detective! My database function won't execute properly!"),
‎            ("Professor Py", "Python is complaining about an unexpected block structure."),
‎            ("Professor Py", "Check the indentation inside this function block.")
‎        ],
‎        "prompt": "def load_data():\n_ _ _ _ print('Data Loaded Successfully')",
‎        "hint": "Hint: Type 4 spaces to complete the block indentation.",
‎        "correct": "    ",
‎        "input_offset_x": 60,
‎        "code_syntax_hint": "indentation"
‎    },
‎    # --- INTERMEDIATE LEVELS ---
‎    {
‎        "difficulty": "Intermediate",
‎        "title": "The Conditional Lock",
‎        "lines": [
‎            ("Sergeant Syntax", "The vault door has a conditional lock! We need the right comparison operator."),
‎            ("Sergeant Syntax", "The code checks if the access code equals '1234' but something's off."),
‎            ("Sergeant Syntax", "Python uses a specific operator for equality checking. Which one is it?")
‎        ],
‎        "prompt": "# Case 4: Fix the comparison!\nif user_code _ '1234':\n    print('Access Granted')",
‎        "hint": "Hint: Assignment uses '=', but comparison uses something else...",
‎        "correct": "==",
‎        "input_offset_x": 145,
‎        "code_syntax_hint": "comparison"
‎    },
‎    {
‎        "difficulty": "Intermediate",
‎        "title": "The List Mystery",
‎        "lines": [
‎            ("Data Clerk Dot", "My shopping list is broken! It keeps saying 'false' for everything!"),
‎            ("Data Clerk Dot", "I need to check if 'eggs' is in the list. The logic makes sense but syntax is wrong."),
‎            ("Data Clerk Dot", "Look at how I'm trying to check membership. Python has a keyword for this!")
‎        ],
‎        "prompt": "# Case 5: Check if 'eggs' is in the list:\nitems = ['milk', 'bread', 'eggs', 'cheese']\nif 'eggs' _ items:",
‎        "hint": "Hint: What keyword checks if a value exists in a collection?",
‎        "correct": "in",
‎        "input_offset_x": 110,
‎        "code_syntax_hint": "keyword"
‎    },
‎    {
‎        "difficulty": "Intermediate",
‎        "title": "The Loop Puzzle",
‎        "lines": [
‎            ("Inspector Iterate", "My counting program threw a syntax error! Numbers won't print themselves!"),
‎            ("Inspector Iterate", "I need to loop through numbers 1 to 5 but I've forgotten the keyword."),
‎            ("Inspector Iterate", "It starts the loop but Python doesn't recognize this structure...")
‎        ],
‎        "prompt": "# Case 6: Complete the for loop:\n_ num in range(1, 6):\n    print(num)",
‎        "hint": "Hint: What keyword begins a for loop in Python?",
‎        "correct": "for",
‎        "input_offset_x": 60,
‎        "code_syntax_hint": "keyword"
‎    },
‎    # --- ADVANCED LEVELS ---
‎    {
‎        "difficulty": "Advanced",
‎        "title": "The Function Return",
‎        "lines": [
‎            ("Captain Callable", "My calculator function won't give me the result! It computes but returns nothing!"),
‎            ("Captain Callable", "The function adds two numbers correctly inside, but the result disappears."),
‎            ("Captain Callable", "I need a keyword that sends the value back to where the function was called.")
‎        ],
‎        "prompt": "def add(a, b):\n    result = a + b\n    _ result",
‎        "hint": "Hint: What keyword sends a value back from a function?",
‎        "correct": "return",
‎        "input_offset_x": 65,
‎        "code_syntax_hint": "keyword"
‎    },
‎    {
‎        "difficulty": "Advanced",
‎        "title": "The Class Definition",
‎        "lines": [
‎            ("Professor Py", "My object-oriented program is incomplete! The blueprint is missing a keyword!"),
‎            ("Professor Py", "I'm defining a new type of object but Python doesn't know where the definition starts."),
‎            ("Professor Py", "Every class needs this keyword before its name. What is it?")
‎        ],
‎        "prompt": "# Case 8: Define the Robot class:\n_ Robot:\n    def __init__(self, name):\n        self.name = name",
‎        "hint": "Hint: What keyword defines a class in Python?",
‎        "correct": "class",
‎        "input_offset_x": 60,
‎        "code_syntax_hint": "keyword"
‎    },
‎    {
‎        "difficulty": "Advanced",
‎        "title": "The Import Statement",
‎        "lines": [
‎            ("Librarian Link", "The code library is locked! I need to import the 'math' module."),
‎            ("Librarian Link", "Python should know this module but it throws a NameError every time."),
‎            ("Librarian Link", "I need the correct keyword to bring in external modules.")
‎        ],
‎        "prompt": "# Case 9: Import the math module:\n_ math",
‎        "hint": "Hint: What keyword brings modules into your Python script?",
‎        "correct": "import",
‎        "input_offset_x": 60,
‎        "code_syntax_hint": "keyword"
‎    },
‎    {
‎        "difficulty": "Advanced",
‎        "title": "The Try-Except Block",
‎        "lines": [
‎            ("Sergeant Syntax", "My program crashes when the user enters invalid input! I need error handling."),
‎            ("Sergeant Syntax", "I need to 'try' something and 'except' errors, but there's a specific keyword order."),
‎            ("Sergeant Syntax", "Look at the try block. What keyword comes after 'try' to handle errors?")
‎        ],
‎        "prompt": "try:\n    number = int(input('Enter a number: '))\n_ ValueError:\n    print('That was not a valid number!')",
‎        "hint": "Hint: What keyword catches exceptions in a try block?",
‎        "correct": "except",
‎        "input_offset_x": 60,
‎        "code_syntax_hint": "keyword"
‎    },
‎    # --- EXPERT LEVELS ---
‎    {
‎        "difficulty": "Expert",
‎        "title": "The List Comprehension",
‎        "lines": [
‎            ("Data Clerk Dot", "I'm trying to square all numbers in a list efficiently!"),
‎            ("Data Clerk Dot", "There's a Pythonic one-liner for this, but I keep getting syntax errors."),
‎            ("Data Clerk Dot", "The expression needs proper brackets. What kind of brackets wrap a list comprehension?")
‎        ],
‎        "prompt": "# Case 11: Square all numbers:\nnums = [1, 2, 3, 4]\nsquares = _ x**2 for x in nums _",
‎        "hint": "Hint: List comprehensions use specific brackets like []",
‎        "correct": "[]",
‎        "input_offset_x": 155,
‎        "code_syntax_hint": "brackets"
‎    },
‎    {
‎        "difficulty": "Expert",
‎        "title": "The Lambda Function",
‎        "lines": [
‎            ("Lambda Larry", "I need a tiny one-line function but I've forgotten the syntax!"),
‎            ("Lambda Larry", "Python has a keyword for anonymous functions. It's short and elegant."),
‎            ("Lambda Larry", "Look at where the function should go. What keyword creates anonymous functions?")
‎        ],
‎        "prompt": "# Case 12: Create a lambda that doubles a number:\ndouble = _ x: x * 2\nprint(double(5))",
‎        "hint": "Hint: What keyword creates anonymous/mini functions in Python?",
‎        "correct": "lambda",
‎        "input_offset_x": 130,
‎        "code_syntax_hint": "keyword"
‎    },
‎    {
‎        "difficulty": "Expert",
‎        "title": "The Decorator Pattern",
‎        "lines": [
‎            ("Professor Py", "My decorator isn't working! The @ symbol needs a proper function after it."),
‎            ("Professor Py", "I've written a logging wrapper but Python doesn't know which function to apply."),
‎            ("Professor Py", "What symbol or keyword decorates a function in Python?")
‎        ],
‎        "prompt": "# Case 13: Apply the timer decorator:\n_ timer\ndef slow_function():\n    print('Processing...')",
‎        "hint": "Hint: Decorators use the @ symbol. What goes after @?",
‎        "correct": "@",
‎        "input_offset_x": 60,
‎        "code_syntax_hint": "symbol"
‎    },
‎]
‎
‎DIFFICULTY_COLORS = {
‎    "Beginner": (92, 144, 116),
‎    "Intermediate": (222, 133, 101),
‎    "Advanced": (74, 96, 122),
‎    "Expert": (204, 91, 91)
‎}
‎
‎class PythonDetectiveGame:
‎    def __init__(self):
‎        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
‎        pygame.display.set_caption("Python Detective - Learn Python Through Mystery!")
‎        self.clock = pygame.time.Clock()
‎        self.running = True
‎        self.state = STATE_MENU
‎
‎        # Fonts
‎        self.font_title = pygame.font.SysFont(None, 48, bold=True)
‎        self.font_title_small = pygame.font.SysFont(None, 36, bold=True)
‎        self.font_body = pygame.font.SysFont(None, 24)
‎        self.font_code = pygame.font.SysFont(None, 26, bold=True)
‎        self.font_small = pygame.font.SysFont(None, 20)
‎        self.font_difficulty = pygame.font.SysFont(None, 18, bold=True)
‎
‎        self.current_quest = 0
‎        self.dialogue_index = 0
‎        self.user_input_text = ""
‎        self.input_active = True
‎        self.feedback_message = ""
‎        self.feedback_color = COLOR_CORRECT
‎        
‎        self.last_dialogue_click = 0
‎        self.dialogue_cooldown = 200
‎        self.quest_buttons = []  # Holds tuple: (rect, actual_global_index)
‎
‎    def run(self):
‎        while self.running:
‎            self.handle_events()
‎            self.update()
‎            self.draw()
‎            self.clock.tick(FPS)
‎        pygame.quit()
‎        sys.exit()
‎
‎    def handle_events(self):
‎        events = pygame.event.get()
‎        for event in events:
‎            if event.type == pygame.QUIT:
‎                self.running = False
‎
‎            if self.state == STATE_MENU:
‎                self._handle_menu_events(event)
‎            elif self.state == STATE_LEVEL_SELECT:
‎                self._handle_level_select_events(event)
‎            elif self.state == STATE_DIALOGUE:
‎                self._handle_dialogue_events(event)
‎            elif self.state == STATE_PUZZLE:
‎                self._handle_puzzle_events(event)
‎            elif self.state == STATE_FEEDBACK:
‎                self._handle_feedback_events(event)
‎            elif self.state == STATE_GAME_OVER:
‎                self._handle_game_over_events(event)
‎
‎    def _handle_menu_events(self, event):
‎        if event.type == pygame.MOUSEBUTTONDOWN:
‎            if self.btn_start_rect.collidepoint(event.pos):
‎                self.state = STATE_LEVEL_SELECT
‎
‎    def _handle_level_select_events(self, event):
‎        if event.type == pygame.MOUSEBUTTONDOWN:
‎            if self.btn_back_rect.collidepoint(event.pos):
‎                self.state = STATE_MENU
‎                return
‎
‎            for btn_rect, actual_idx in self.quest_buttons:
‎                if btn_rect.collidepoint(event.pos):
‎                    if actual_idx < len(QUESTS):
‎                        self.current_quest = actual_idx
‎                        self.dialogue_index = 0
‎                        self.user_input_text = ""
‎                        self.input_active = True
‎                        self.state = STATE_DIALOGUE
‎                        return
‎
‎    def _handle_dialogue_events(self, event):
‎        if self.current_quest >= len(QUESTS):
‎            return
‎        current_data = QUESTS[self.current_quest]
‎        if event.type == pygame.MOUSEBUTTONDOWN:
‎            now = pygame.time.get_ticks()
‎            if now - self.last_dialogue_click > self.dialogue_cooldown:
‎                self.last_dialogue_click = now
‎                self._advance_dialogue(current_data)
‎        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
‎            self._advance_dialogue(current_data)
‎
‎    def _advance_dialogue(self, current_data):
‎        self.dialogue_index += 1
‎        if self.dialogue_index >= len(current_data["lines"]):
‎            self.state = STATE_PUZZLE
‎            pygame.key.start_text_input()
‎
‎    def _handle_puzzle_events(self, event):
‎        if event.type == pygame.KEYDOWN:
‎            if event.key == pygame.K_BACKSPACE:
‎                self.user_input_text = self.user_input_text[:-1]
‎            elif event.key == pygame.K_RETURN:
‎                self.check_puzzle_answer()
‎            elif event.key == pygame.K_ESCAPE:
‎                pygame.key.stop_text_input()
‎                self.state = STATE_LEVEL_SELECT
‎            else:
‎                if event.unicode and event.unicode.isprintable():
‎                    if len(self.user_input_text) < 12:
‎                        self.user_input_text += event.unicode
‎        elif event.type == pygame.MOUSEBUTTONDOWN:
‎            if self.btn_submit_rect.collidepoint(event.pos):
‎                self.check_puzzle_answer()
‎
‎    def _handle_feedback_events(self, event):
‎        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
‎            if self.feedback_message == "Correct!":
‎                self.current_quest += 1
‎                self.dialogue_index = 0
‎                self.user_input_text = ""
‎                if self.current_quest >= len(QUESTS):
‎                    self.state = STATE_GAME_OVER
‎                    pygame.key.stop_text_input()
‎                else:
‎                    self.state = STATE_LEVEL_SELECT
‎            else:
‎                self.state = STATE_PUZZLE
‎
‎    def _handle_game_over_events(self, event):
‎        if event.type == pygame.MOUSEBUTTONDOWN:
‎            if self.btn_restart_rect.collidepoint(event.pos):
‎                self.current_quest = 0
‎                self.state = STATE_MENU
‎
‎    def check_puzzle_answer(self):
‎        if self.current_quest >= len(QUESTS):
‎            return
‎        current_data = QUESTS[self.current_quest]
‎        if self.user_input_text.strip() == current_data["correct"].strip():
‎            self.feedback_message = "Correct!"
‎            self.feedback_color = COLOR_CORRECT
‎        else:
‎            self.feedback_message = "Incorrect! Try again."
‎            self.feedback_color = COLOR_INCORRECT
‎        self.state = STATE_FEEDBACK
‎
‎    def update(self):
‎        pass
‎
‎    def draw(self):
‎        self.screen.fill(COLOR_BG)
‎        if self.state == STATE_MENU:
‎            self.draw_menu()
‎        elif self.state == STATE_LEVEL_SELECT:
‎            self.draw_level_select()
‎        elif self.state == STATE_DIALOGUE:
‎            self.draw_dialogue()
‎        elif self.state == STATE_PUZZLE:
‎            self.draw_puzzle()
‎        elif self.state == STATE_FEEDBACK:
‎            self.draw_feedback()
‎        elif self.state == STATE_GAME_OVER:
‎            self.draw_game_over()
‎        pygame.display.flip()
‎
‎    def draw_menu(self):
‎        pygame.draw.circle(self.screen, (235, 225, 210), (150, 100), 80)
‎        pygame.draw.circle(self.screen, (230, 220, 200), (800, 450), 120)
‎        title_surf = self.font_title.render("PYTHON DETECTIVE", True, COLOR_PRIMARY)
‎        self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 20)))
‎        subtitle_surf = self.font_body.render("Learn Python Through Cozy Mystery Adventures", True, COLOR_TEXT_DARK)
‎        self.screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 40)))
‎        
‎        diff_surf = self.font_small.render(f"{len(QUESTS)} Cases Across All Levels", True, COLOR_TEXT_DARK)
‎        self.screen.blit(diff_surf, diff_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 70)))
‎
‎        self.btn_start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40, 240, 50)
‎        pygame.draw.rect(self.screen, COLOR_ACCENT, self.btn_start_rect, border_radius=8)
‎        btn_text = self.font_body.render("Start Investigation", True, COLOR_TEXT_LIGHT)
‎        self.screen.blit(btn_text, btn_text.get_rect(center=self.btn_start_rect.center))
‎
‎    def draw_level_select(self):
‎        header_surf = self.font_title_small.render("SELECT A CASE", True, COLOR_PRIMARY)
‎        self.screen.blit(header_surf, (40, 30))
‎
‎        self.btn_back_rect = pygame.Rect(SCREEN_WIDTH - 140, 30, 100, 36)
‎        pygame.draw.rect(self.screen, COLOR_PRIMARY, self.btn_back_rect, border_radius=6)
‎        back_text = self.font_small.render("Back", True, COLOR_TEXT_LIGHT)
‎        self.screen.blit(back_text, back_text.get_rect(center=self.btn_back_rect.center))
‎
‎        y_offset = 90
‎        self.quest_buttons = []
‎
‎        # Safe iteration using global list index directly instead of .index() lookup
‎        for idx, quest in enumerate(QUESTS):
‎            diff = quest["difficulty"]
‎            diff_color = DIFFICULTY_COLORS.get(diff, COLOR_PRIMARY)
‎
‎            # Draw a difficulty divider if it's the first element of that category
‎            if idx == 0 or QUESTS[idx - 1]["difficulty"] != diff:
‎                y_offset += 10
‎                diff_surf = self.font_difficulty.render(f"── {diff.upper()} ──", True, diff_color)
‎                self.screen.blit(diff_surf, (50, y_offset))
‎                y_offset += 25
‎
‎            btn_rect = pygame.Rect(60, y_offset, SCREEN_WIDTH - 140, 32)
‎            pygame.draw.rect(self.screen, COLOR_PANEL, btn_rect, border_radius=6)
‎            pygame.draw.rect(self.screen, diff_color, btn_rect, width=1, border_radius=6)
‎
‎            label = f"#{idx + 1}: {quest['title']}"
‎            label_surf = self.font_body.render(label, True, COLOR_TEXT_DARK)
‎            self.screen.blit(label_surf, (75, y_offset + 3))
‎
‎            hint_tag = f"[{quest['code_syntax_hint']}]"
‎            hint_surf = self.font_small.render(hint_tag, True, diff_color)
‎            self.screen.blit(hint_surf, (SCREEN_WIDTH - 190, y_offset + 5))
‎
‎            self.quest_buttons.append((btn_rect, idx))
‎            y_offset += 38
‎
‎    def draw_dialogue(self):
‎        if self.current_quest >= len(QUESTS):
‎            return
‎        current_data = QUESTS[self.current_quest]
‎        pygame.draw.rect(self.screen, (220, 230, 235), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
‎
‎        badge_rect = pygame.Rect(40, 30, 140, 32)
‎        pygame.draw.rect(self.screen, COLOR_PRIMARY, badge_rect, border_radius=8)
‎        badge_text = self.font_small.render(f"Case #{self.current_quest + 1}", True, COLOR_TEXT_LIGHT)
‎        self.screen.blit(badge_text, (badge_rect.x + 15, badge_rect.y + 6))
‎
‎        diff_color = DIFFICULTY_COLORS.get(current_data["difficulty"], COLOR_PRIMARY)
‎        diff_rect = pygame.Rect(190, 30, 100, 32)
‎        pygame.draw.rect(self.screen, diff_color, diff_rect, border_radius=8)
‎        diff_text = self.font_small.render(current_data["difficulty"], True, COLOR_TEXT_LIGHT)
‎        self.screen.blit(diff_text, (diff_rect.x + 15, diff_rect.y + 6))
‎
‎        portrait_rect = pygame.Rect(80, 90, 180, 250)
‎        pygame.draw.rect(self.screen, COLOR_ACCENT, portrait_rect, border_radius=12)
‎        p_label = self.font_body.render("[Character]", True, COLOR_TEXT_LIGHT)
‎        self.screen.blit(p_label, p_label.get_rect(center=(portrait_rect.centerx, portrait_rect.centery - 15)))
‎        
‎        speaker_name = current_data["lines"][self.dialogue_index][0]
‎        name_surf = self.font_small.render(speaker_name, True, COLOR_TEXT_LIGHT)
‎        self.screen.blit(name_surf, name_surf.get_rect(center=(portrait_rect.centerx, portrait_rect.centery + 25)))
‎
‎        dialogue_box = pygame.Rect(40, 360, SCREEN_WIDTH - 80, 130)
‎        surf_panel = pygame.Surface((dialogue_box.width, dialogue_box.height), pygame.SRCALPHA)
‎        surf_panel.fill(COLOR_PANEL)
‎        self.screen.blit(surf_panel, (dialogue_box.x, dialogue_box.y))
‎        pygame.draw.rect(self.screen, COLOR_PRIMARY, dialogue_box, width=3, border_radius=10)
‎
‎        speaker, text = current_data["lines"][self.dialogue_index]
‎        speaker_surf = self.font_body.render(speaker, True, COLOR_ACCENT)
‎        self.screen.blit(speaker_surf, (dialogue_box.x + 20, dialogue_box.y + 15))
‎
‎        self._draw_wrapped_text(text, self.font_body, COLOR_TEXT_DARK, (dialogue_box.x + 20, dialogue_box.y + 55), dialogue_box.width - 40)
‎        hint_surf = self.font_small.render("Press SPACE or Tap to continue...", True, (130, 140, 150))
‎        self.screen.blit(hint_surf, (dialogue_box.right - 260, dialogue_box.bottom - 25))
‎
‎    def _draw_wrapped_text(self, text, font, color, pos, max_width):
‎        words = text.split(' ')
‎        lines = []
‎        current_line = ""
‎        for word in words:
‎            test_line = current_line + word + " "
‎            if font.size(test_line)[0] < max_width:
‎                current_line = test_line
‎            else:
‎                lines.append(current_line)
‎                current_line = word + " "
‎        lines.append(current_line)
‎
‎        y = pos[1]
‎        for line in lines:
‎            surf = font.render(line.strip(), True, color)
‎            self.screen.blit(surf, (pos[0], y))
‎            y += font.get_height() + 2
‎
‎    def draw_puzzle(self):
‎        if self.current_quest >= len(QUESTS):
‎            return
‎        current_data = QUESTS[self.current_quest]
‎        diff_color = DIFFICULTY_COLORS.get(current_data["difficulty"], COLOR_PRIMARY)
‎
‎        case_header = f"CASE #{self.current_quest + 1}: {current_data['title']}"
‎        self.screen.blit(self.font_body.render(case_header, True, diff_color), (40, 25))
‎
‎        editor_rect = pygame.Rect(40, 65, SCREEN_WIDTH - 80, 220)
‎        pygame.draw.rect(self.screen, COLOR_EDITOR_BG, editor_rect, border_radius=8)
‎
‎        line_num_rect = pygame.Rect(40, 65, 40, 220)
‎        pygame.draw.rect(self.screen, (28, 34, 42), line_num_rect, border_radius=8)
‎
‎        lines = current_data["prompt"].split('\n')
‎        input_row_idx = 1 if len(lines) > 1 and "_" in lines[1] else 0
‎
‎        for idx, line in enumerate(lines):
‎            line_num_surf = self.font_small.render(str(idx + 1), True, (90, 100, 110))
‎            self.screen.blit(line_num_surf, (52 - line_num_surf.get_width(), 95 + (idx * 35)))
‎
‎            if "#" in line:
‎                color = COLOR_CODE_GREEN
‎            elif "def " in line or "class " in line or "if " in line:
‎                color = COLOR_CODE_BLUE
‎            elif "print" in line or "'" in line or '"' in line:
‎                color = COLOR_CODE_YELLOW
‎            else:
‎                color = COLOR_TEXT_LIGHT
‎
‎            self.screen.blit(self.font_code.render(line, True, color), (60, 95 + (idx * 35)))
‎
‎        # Dynamic and fixed input box rendering loop based on target line position
‎        input_box_rect = pygame.Rect(
‎            current_data["input_offset_x"],
‎            95 + (input_row_idx * 35),
‎            max(100, len(current_data["correct"]) * 18),
‎            32
‎        )
‎
‎        pygame.draw.rect(self.screen, (50, 60, 75), input_box_rect, border_radius=4)
‎        pygame.draw.rect(self.screen, COLOR_ACCENT, input_box_rect, width=2, border_radius=4)
‎
‎        input_surf = self.font_code.render(self.user_input_text, True, COLOR_ACCENT)
‎        self.screen.blit(input_surf, (input_box_rect.x + 8, input_box_rect.y + 2))
‎
‎        if (pygame.time.get_ticks() // 500) % 2 == 0 and self.state == STATE_PUZZLE:
‎            cursor_x = input_box_rect.x + 8 + self.font_code.size(self.user_input_text)[0]
‎            pygame.draw.line(self.screen, COLOR_ACCENT, (cursor_x, input_box_rect.y + 4), (cursor_x, input_box_rect.y + 28), 2)
‎
‎        hint_box = pygame.Rect(40, 305, SCREEN_WIDTH - 80, 50)
‎        pygame.draw.rect(self.screen, (240, 235, 220), hint_box, border_radius=6)
‎        self.screen.blit(self.font_small.render(current_data["hint"], True, COLOR_TEXT_DARK), (hint_box.x + 15, hint_box.y + 15))
‎
‎        self.screen.blit(self.font_small.render("Press ESC to go back", True, (150, 150, 150)), (40, 370))
‎
‎        self.btn_submit_rect = pygame.Rect(SCREEN_WIDTH - 220, 420, 180, 50)
‎        pygame.draw.rect(self.screen, COLOR_PRIMARY, self.btn_submit_rect, border_radius=8)
‎        submit_text = self.font_body.render("Submit Patch", True, COLOR_TEXT_LIGHT)
‎        self.screen.blit(submit_text, submit_text.get_rect(center=self.btn_submit_rect.center))
‎
‎    def draw_feedback(self):
‎        dim_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
‎        dim_surf.set_alpha(128)
‎        dim_surf.fill((0, 0, 0))
‎        self.screen.blit(dim_surf, (0, 0))
‎
‎        modal_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 200)
‎        pygame.draw.rect(self.screen, COLOR_BG, modal_rect, border_radius=12)
‎        pygame.draw.rect(self.screen, self.feedback_color, modal_rect, width=4, border_radius=12)
‎
‎        icon = "✓" if self.feedback_message == "Correct!" else "✗"
‎        icon_surf = self.font_title.render(icon, True, self.feedback_color)
‎        self.screen.blit(icon_surf, icon_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
‎
‎        msg_surf = self.font_title_small.render(self.feedback_message, True, self.feedback_color)
‎        self.screen.blit(msg_surf, msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10)))
‎
‎        sub_text = "Tap / Space to continue" if self.feedback_message == "Correct!" else "Tap / Space to try again"
‎        sub_surf = self.font_body.render(sub_text, True, COLOR_TEXT_DARK)
‎        self.screen.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))
‎
‎        if self.feedback_message != "Correct!" and self.current_quest < len(QUESTS):
‎            correct = QUESTS[self.current_quest]["correct"]
‎            correct_text = "Hint: Need 4 spaces (type them!)" if correct == " " * 4 else f"Hint: The answer is {len(correct)} character(s) long"
‎            hint_surf = self.font_small.render(correct_text, True, (150, 150, 150))
‎            self.screen.blit(hint_surf, hint_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)))
‎
‎    def draw_game_over(self):
‎        pygame.draw.rect(self.screen, (240, 235, 220), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
‎        title_surf = self.font_title.render("ALL CASES SOLVED!", True, COLOR_CORRECT)
‎        self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 30)))
‎
‎        badge_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 3 + 10, 150, 150)
‎        pygame.draw.rect(self.screen, (255, 215, 0), badge_rect, border_radius=20)
‎        pygame.draw.rect(self.screen, (200, 160, 0), badge_rect, width=4, border_radius=20)
‎        
‎        badge_text = self.font_title_small.render("⭐", True, (200, 120, 0))
‎        self.screen.blit(badge_text, badge_text.get_rect(center=badge_rect.center))
‎
‎        msg_surf = self.font_body.render(f"You solved all {len(QUESTS)} cases and saved Python Town!", True, COLOR_TEXT_DARK)
‎        self.screen.blit(msg_surf, msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110)))
‎
‎        self.btn_restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50)
‎        pygame.draw.rect(self.screen, COLOR_PRIMARY, self.btn_restart_rect, border_radius=8)
‎        restart_text = self.font_body.render("Main Menu", True, COLOR_TEXT_LIGHT)
‎        self.screen.blit(restart_text, restart_text.get_rect(center=self.btn_restart_rect.center))
‎
‎if __name__ == "__main__":
‎    game = PythonDetectiveGame()
‎    game.run()
‎
