# main.py - Kivy version of Python Detective Game
import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import sys

# Game colors
COLOR_BG = (0.96, 0.94, 0.90, 1)
COLOR_PRIMARY = (0.29, 0.38, 0.48, 1)
COLOR_ACCENT = (0.87, 0.52, 0.40, 1)
COLOR_CORRECT = (0.36, 0.56, 0.45, 1)
COLOR_INCORRECT = (0.80, 0.36, 0.36, 1)

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_quest = 0
        self.dialogue_index = 0
        self.user_input = ""
        self.state = "menu"
        
        self.quests = self.get_quests()
        self.setup_ui()
    
    def get_quests(self):
        return [
            {
                "title": "The Clock Tower",
                "lines": [
                    ("Mayor Pip", "The town clock stopped! Fix the print statement!"),
                    ("Mayor Pip", "It's missing something at the end..."),
                ],
                "code": "print('System Active' _",
                "correct": ")",
                "hint": "How do you close a function call?"
            },
            {
                "title": "The Security Gate",
                "lines": [
                    ("Chief Codey", "The gate variable assignment is broken!"),
                    ("Chief Codey", "What operator assigns values?"),
                ],
                "code": "gate_status _ 'open'",
                "correct": "=",
                "hint": "Assignment operator?"
            },
            {
                "title": "The Database Function",
                "lines": [
                    ("Professor Py", "My function needs proper indentation!"),
                    ("Professor Py", "Type 4 spaces to indent"),
                ],
                "code": "def load_data():\n_ _ _ _ print('Loaded')",
                "correct": "    ",
                "hint": "Need 4 spaces"
            },
            {
                "title": "The Conditional Lock",
                "lines": [
                    ("Sergeant Syntax", "Fix the comparison operator!"),
                    ("Sergeant Syntax", "How do we check equality in Python?"),
                ],
                "code": "if user_code _ '1234':",
                "correct": "==",
                "hint": "Double equals?"
            },
            {
                "title": "The List Membership",
                "lines": [
                    ("Data Clerk Dot", "Check if 'eggs' is in the list!"),
                    ("Data Clerk Dot", "What keyword checks membership?"),
                ],
                "code": "if 'eggs' _ items:",
                "correct": "in",
                "hint": "Membership keyword?"
            },
        ]
    
    def setup_ui(self):
        with self.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(size=Window.size)
        
        Window.bind(size=self._update_bg)
        self.show_menu()
    
    def _update_bg(self, instance, value):
        self.bg.size = value
    
    def show_menu(self):
        self.clear_widgets()
        self.state = "menu"
        
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        title = Label(
            text="PYTHON DETECTIVE",
            font_size=dp(36),
            bold=True,
            color=COLOR_PRIMARY,
            size_hint_y=0.3
        )
        
        subtitle = Label(
            text="Cozy Mystery Programming Adventure\nLearn Python on Your Phone!",
            font_size=dp(18),
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=0.2
        )
        
        start_btn = Button(
            text="Start Investigation",
            size_hint=(0.6, 0.15),
            pos_hint={'center_x': 0.5},
            background_color=COLOR_ACCENT,
            color=(1,1,1,1),
            font_size=dp(20)
        )
        start_btn.bind(on_press=self.start_game)
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(Label(size_hint_y=0.2))
        layout.add_widget(start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.current_quest = 0
        self.dialogue_index = 0
        self.user_input = ""
        self.show_dialogue()
    
    def show_dialogue(self):
        self.clear_widgets()
        self.state = "dialogue"
        
        quest = self.quests[self.current_quest]
        speaker, text = quest["lines"][self.dialogue_index]
        
        layout = BoxLayout(orientation='vertical', padding=20)
        
        # Header
        header = Label(
            text=f"Case #{self.current_quest + 1}: {quest['title']}",
            font_size=dp(18),
            bold=True,
            color=COLOR_PRIMARY,
            size_hint_y=0.15
        )
        
        # Dialogue box
        dialogue_box = BoxLayout(
            orientation='vertical',
            size_hint_y=0.6,
            padding=20,
            spacing=10
        )
        
        with dialogue_box.canvas.before:
            Color(1, 1, 1, 0.9)
            RoundedRectangle(pos=dialogue_box.pos, size=dialogue_box.size, radius=[10])
            Color(*COLOR_PRIMARY)
            RoundedRectangle(pos=dialogue_box.pos, size=dialogue_box.size, radius=[10], width=3)
        
        speaker_label = Label(
            text=f"[b]{speaker}[/b]",
            font_size=dp(16),
            color=COLOR_ACCENT,
            markup=True,
            size_hint_y=0.2,
            halign='left'
        )
        
        text_label = Label(
            text=text,
            font_size=dp(18),
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=0.6,
            halign='center',
            valign='middle'
        )
        
        continue_btn = Button(
            text="Continue (Tap)",
            size_hint=(0.4, 0.15),
            pos_hint={'center_x': 0.5},
            background_color=COLOR_PRIMARY,
            color=(1,1,1,1)
        )
        continue_btn.bind(on_press=self.advance_dialogue)
        
        dialogue_box.add_widget(speaker_label)
        dialogue_box.add_widget(text_label)
        
        layout.add_widget(header)
        layout.add_widget(dialogue_box)
        layout.add_widget(continue_btn)
        
        self.add_widget(layout)
    
    def advance_dialogue(self, instance):
        self.dialogue_index += 1
        quest = self.quests[self.current_quest]
        
        if self.dialogue_index >= len(quest["lines"]):
            self.show_puzzle()
        else:
            self.show_dialogue()
    
    def show_puzzle(self):
        self.clear_widgets()
        self.state = "puzzle"
        
        quest = self.quests[self.current_quest]
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header
        header = Label(
            text=f"Solve Case #{self.current_quest + 1}",
            font_size=dp(20),
            bold=True,
            color=COLOR_PRIMARY,
            size_hint_y=0.1
        )
        
        # Code display
        code_box = BoxLayout(
            orientation='vertical',
            size_hint_y=0.5,
            padding=15,
            spacing=5
        )
        
        with code_box.canvas.before:
            Color(0.13, 0.16, 0.19, 1)
            RoundedRectangle(pos=code_box.pos, size=code_box.size, radius=[8])
        
        code_label = Label(
            text=quest["code"],
            font_size=dp(16),
            color=(0.56, 0.89, 0.71, 1),
            halign='left',
            valign='middle',
            text_size=(Window.width - dp(70), None),
            markup=True
        )
        code_box.add_widget(code_label)
        
        # Input section
        input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.15,
            spacing=10
        )
        
        self.text_input = TextInput(
            text=self.user_input,
            hint_text='Type answer here...',
            font_size=dp(18),
            size_hint_x=0.7,
            background_color=(0.2, 0.2, 0.25, 1),
            foreground_color=(1, 0.6, 0.3, 1),
            cursor_color=(1, 0.6, 0.3, 1)
        )
        self.text_input.bind(text=self.on_text_change)
        
        submit_btn = Button(
            text="Submit",
            size_hint_x=0.3,
            background_color=COLOR_PRIMARY,
            color=(1,1,1,1)
        )
        submit_btn.bind(on_press=self.check_answer)
        
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(submit_btn)
        
        # Hint
        hint_label = Label(
            text=f"💡 {quest['hint']}",
            font_size=dp(14),
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=0.1
        )
        
        layout.add_widget(header)
        layout.add_widget(code_box)
        layout.add_widget(input_layout)
        layout.add_widget(hint_label)
        
        self.add_widget(layout)
    
    def on_text_change(self, instance, value):
        self.user_input = value
    
    def check_answer(self, instance):
        quest = self.quests[self.current_quest]
        
        if self.user_input.strip() == quest["correct"].strip():
            self.show_feedback(True)
        else:
            self.show_feedback(False)
    
    def show_feedback(self, is_correct):
        self.clear_widgets()
        self.state = "feedback"
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        if is_correct:
            msg = "CORRECT! 🎉"
            color = COLOR_CORRECT
        else:
            msg = "INCORRECT! Try Again"
            color = COLOR_INCORRECT
        
        feedback_label = Label(
            text=msg,
            font_size=dp(32),
            bold=True,
            color=color,
            size_hint_y=0.3
        )
        
        next_btn = Button(
            text="Continue",
            size_hint=(0.5, 0.15),
            pos_hint={'center_x': 0.5},
            background_color=COLOR_PRIMARY,
            color=(1,1,1,1)
        )
        
        if is_correct:
            next_btn.bind(on_press=self.next_quest)
        else:
            next_btn.bind(on_press=self.retry_quest)
        
        layout.add_widget(Label(size_hint_y=0.2))
        layout.add_widget(feedback_label)
        layout.add_widget(next_btn)
        
        self.add_widget(layout)
    
    def next_quest(self, instance):
        self.current_quest += 1
        self.dialogue_index = 0
        self.user_input = ""
        
        if self.current_quest >= len(self.quests):
            self.show_victory()
        else:
            self.show_dialogue()
    
    def retry_quest(self, instance):
        self.dialogue_index = 0
        self.user_input = ""
        self.show_puzzle()
    
    def show_victory(self):
        self.clear_widgets()
        self.state = "victory"
        
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        title = Label(
            text="ALL CASES SOLVED! 🏆",
            font_size=dp(36),
            bold=True,
            color=COLOR_CORRECT,
            size_hint_y=0.3
        )
        
        msg = Label(
            text="You saved Python Town, Master Detective!\n\nYou've learned:\n• Print statements\n• Variable assignment\n• Indentation\n• Comparison operators\n• Membership operators",
            font_size=dp(18),
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=0.4,
            halign='center'
        )
        
        restart_btn = Button(
            text="Play Again",
            size_hint=(0.5, 0.15),
            pos_hint={'center_x': 0.5},
            background_color=COLOR_PRIMARY,
            color=(1,1,1,1)
        )
        restart_btn.bind(on_press=lambda x: self.show_menu())
        
        layout.add_widget(title)
        layout.add_widget(msg)
        layout.add_widget(restart_btn)
        
        self.add_widget(layout)


class PythonDetectiveApp(App):
    def build(self):
        return GameWidget()


if __name__ == '__main__':
    PythonDetectiveApp().run()
