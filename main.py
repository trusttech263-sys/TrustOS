import os
import json
import ast
import operator
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window

THEMES = {
    "Luxury": {
        "bg": (0.025, 0.018, 0.055, 1),
        "panel": (0.095, 0.065, 0.16, 1),
        "accent": (0.68, 0.39, 0.98, 1),
        "text": (0.97, 0.96, 1, 1),
        "muted": (0.68, 0.64, 0.76, 1)
    },
    "Minimal": {
        "bg": (0.93, 0.94, 0.97, 1),
        "panel": (1, 1, 1, 1),
        "accent": (0.25, 0.34, 0.72, 1),
        "text": (0.08, 0.09, 0.14, 1),
        "muted": (0.40, 0.42, 0.49, 1)
    },
    "Cyber": {
        "bg": (0.008, 0.018, 0.045, 1),
        "panel": (0.025, 0.075, 0.12, 1),
        "accent": (0.0, 0.86, 1.0, 1),
        "text": (0.72, 1.0, 0.94, 1),
        "muted": (0.34, 0.72, 0.78, 1)
    }
}

class Surface(BoxLayout):
    def __init__(self, color, radius=18, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._color = Color(*color)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size,
                                           radius=[dp(radius)])
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *_):
        self._rect.pos = self.pos
        self._rect.size = self.size

class TrustButton(Button):
    def __init__(self, title, colors, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.text = title
        self.font_size = sp(13)
        self.bold = True
        self.color = colors["text"]
        self.background_normal = ""
        self.background_down = ""
        self.background_color = colors["panel"]
        if callback:
            self.bind(on_release=lambda *_: callback())

class TrustOS(App):
    def build(self):
        self.title = "TrustOS"
        self.data_dir = self.user_data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.settings_path = os.path.join(self.data_dir, "settings.json")
        self.notes_path = os.path.join(self.data_dir, "notes.txt")
        self.theme = "Luxury"
        self.mode = "mobile"
        self._load_settings()
        self.colors = THEMES[self.theme]

        self.manager = ScreenManager(transition=FadeTransition(duration=0.22))
        self._build_boot()
        self._build_home("mobile")
        self._build_home("desktop")
        Clock.schedule_once(self._finish_boot, 1.8)
        Clock.schedule_interval(self._tick, 1)
        return self.manager

    def _load_settings(self):
        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.theme = data.get("theme", "Luxury")
            self.mode = data.get("mode", "mobile")
            if self.theme not in THEMES:
                self.theme = "Luxury"
            if self.mode not in ("mobile", "desktop"):
                self.mode = "mobile"
        except (OSError, ValueError, TypeError):
            pass

    def _save_settings(self):
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump({"theme": self.theme, "mode": self.mode}, f)

    def _screen(self, name):
        screen = Screen(name=name)
        with screen.canvas.before:
            screen._bg_color = Color(*self.colors["bg"])
            screen._bg_rect = RoundedRectangle(pos=screen.pos, size=screen.size)
        screen.bind(pos=lambda w, p: setattr(w._bg_rect, "pos", p),
                    size=lambda w, s: setattr(w._bg_rect, "size", s))
        self.manager.add_widget(screen)
        return screen

    def _build_boot(self):
        screen = self._screen("boot")
        layout = BoxLayout(orientation="vertical", padding=dp(28), spacing=dp(12))
        layout.add_widget(Label())
        logo = Label(text="TRUSTOS", font_size=sp(38), bold=True,
                     color=self.colors["accent"], size_hint_y=None, height=dp(65))
        layout.add_widget(logo)
        layout.add_widget(Label(text="YOUR WORLD. YOUR SYSTEM.",
                                font_size=sp(11), color=self.colors["text"],
                                size_hint_y=None, height=dp(30)))
        status = Label(text="INITIALIZING TRUSTTECH SYSTEM",
                       font_size=sp(10), color=self.colors["muted"],
                       size_hint_y=None, height=dp(35))
        layout.add_widget(status)
        layout.add_widget(Label())
        layout.add_widget(Label(text="TRUSTTECH  •  VERSION 2.0",
                                font_size=sp(10), color=self.colors["muted"],
                                size_hint_y=None, height=dp(28)))
        screen.add_widget(layout)
        Animation(opacity=0.45, duration=0.8) + Animation(opacity=1, duration=0.8)
        Animation(opacity=0.45, duration=0.8).start(logo)

    def _finish_boot(self, _):
        self.manager.current = self.mode

    def _header(self, title):
        row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        row.add_widget(Label(text=title, bold=True, font_size=sp(17),
                             color=self.colors["accent"], halign="left"))
        clock = Label(text=datetime.now().strftime("%H:%M"),
                      font_size=sp(11), color=self.colors["text"],
                      size_hint_x=0.38)
        row.add_widget(clock)
        return row, clock

    def _app_card(self, name, subtitle, callback):
        card = Surface(self.colors["panel"], orientation="vertical",
                       padding=dp(9), spacing=dp(4))
        card.add_widget(Label(text=name, bold=True, font_size=sp(13),
                              color=self.colors["accent"]))
        card.add_widget(Label(text=subtitle, font_size=sp(10),
                              color=self.colors["muted"), halign="center"))
        card.add_widget(TrustButton("OPEN", self.colors, callback,
                                    size_hint_y=None, height=dp(34)))
        return card

    def _build_home(self, mode):
        screen = self._screen(mode)
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        header, clock = self._header("TRUSTOS")
        if mode == "mobile":
            self.mobile_clock = clock
        else:
            self.desktop_clock = clock
        root.add_widget(header)

        hero = Surface(self.colors["panel"], orientation="vertical",
                       padding=dp(14), spacing=dp(3),
                       size_hint_y=None, height=dp(112))
        hero.add_widget(Label(text="WELCOME TO TRUSTOS", bold=True,
                              font_size=sp(11), color=self.colors["accent"]))
        hero.add_widget(Label(text="Your digital world.", bold=True,
                              font_size=sp(23), color=self.colors["text"]))
        hero.add_widget(Label(text="A personal workspace by TrustTech",
                              font_size=sp(10), color=self.colors["muted"]))
        root.add_widget(hero)

        grid = GridLayout(cols=2, spacing=dp(9))
        apps = [
            ("TrustFiles", "File access", lambda: self._message(
                "TrustFiles", "The file manager module is planned for a later update.")),
            ("TrustNotes", "Write and save", self._notes),
            ("TrustCalc", "Quick calculations", self._calculator),
            ("TrustMusic", "Music library", lambda: self._message(
                "TrustMusic", "The music player module is planned for a later update.")),
            ("TrustAI", "Assistant workspace", lambda: self._message(
                "TrustAI", "TrustAI integration is planned for a later update.")),
            ("Settings", "Themes and layout", self._settings)
        ]
        for name, subtitle, action in apps:
            grid.add_widget(self._app_card(name, subtitle, action))
        root.add_widget(grid)

        footer = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(7))
        footer.add_widget(TrustButton("MOBILE", self.colors,
                                      lambda: self._switch("mobile")))
        footer.add_widget(TrustButton("DESKTOP", self.colors,
                                      lambda: self._switch("desktop")))
        footer.add_widget(TrustButton("ABOUT", self.colors, self._about))
        root.add_widget(footer)
        screen.add_widget(root)

    def _tick(self, _):
        stamp = datetime.now().strftime("%H:%M  •  %d %b")
        for attr in ("mobile_clock", "desktop_clock"):
            widget = getattr(self, attr, None)
            if widget:
                widget.text = stamp

    def _switch(self, mode):
        self.mode = mode
        self._save_settings()
        self.manager.current = mode

    def _message(self, title, body):
        box = BoxLayout(padding=dp(14))
        box.add_widget(Label(text=body, color=self.colors["text"],
                             halign="center"))
        Popup(title=title, content=box, size_hint=(0.86, 0.36)).open()

    def _about(self):
        self._message("About TrustOS",
                      "TrustOS 2.0\\nA hybrid-style Android workspace.\\nDeveloped by Trust Chakanyuka • TrustTech")

    def _settings(self):
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        popup = Popup(title="APPEARANCE", content=box, size_hint=(0.88, 0.55))
        box.add_widget(Label(text="Choose your TrustOS theme",
                             color=self.colors["text"]))
        for theme in THEMES:
            box.add_widget(TrustButton(theme.upper(), self.colors,
                                       lambda t=theme: self._change_theme(t),
                                       size_hint_y=None, height=dp(44)))
        box.add_widget(TrustButton("CLOSE", self.colors, popup.dismiss,
                                   size_hint_y=None, height=dp(42)))
        popup.open()

    def _change_theme(self, theme):
        self.theme = theme
        self._save_settings()
        self.colors = THEMES[theme]
        current_mode = self.mode
        self.manager.clear_widgets()
        self._build_boot()
        self._build_home("mobile")
        self._build_home("desktop")
        self.manager.current = current_mode
        self._message("Theme updated", "TrustOS is now using " + theme + " mode.")

    def _notes(self):
        editor = TextInput(multiline=True, hint_text="Write your notes here...",
                           background_color=self.colors["panel"],
                           foreground_color=self.colors["text"],
                           cursor_color=self.colors["accent"])
        try:
            with open(self.notes_path, "r", encoding="utf-8") as f:
                editor.text = f.read()
        except OSError:
            pass
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        popup = Popup(title="TRUSTNOTES", content=box, size_hint=(0.92, 0.78))
        box.add_widget(editor)
        def save():
            with open(self.notes_path, "w", encoding="utf-8") as f:
                f.write(editor.text)
            popup.dismiss()
            self._message("TrustNotes", "Your notes have been saved on this device.")
        box.add_widget(TrustButton("SAVE NOTES", self.colors, save,
                                   size_hint_y=None, height=dp(46)))
        popup.open()

    def _calculator(self):
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        expression = TextInput(hint_text="Example: 24 * (3 + 2)",
                               multiline=False, size_hint_y=None, height=dp(48))
        result = Label(text="Result appears here", color=self.colors["accent"],
                       font_size=sp(18))
        box.add_widget(expression)
        box.add_widget(TrustButton("CALCULATE", self.colors,
                                   lambda: self._calculate(expression.text, result),
                                   size_hint_y=None, height=dp(46)))
        box.add_widget(result)
        Popup(title="TRUST CALCULATOR", content=box,
              size_hint=(0.9, 0.43)).open()

    def _calculate(self, expression, result):
        ops = {ast.Add: operator.add, ast.Sub: operator.sub,
               ast.Mult: operator.mul, ast.Div: operator.truediv,
               ast.Pow: operator.pow, ast.USub: operator.neg,
               ast.Mod: operator.mod}
        def evaluate(node):
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in ops:
                return ops[type(node.op)](evaluate(node.left), evaluate(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in ops:
                return ops[type(node.op)](evaluate(node.operand))
            raise ValueError("Unsupported expression")
        try:
            answer = evaluate(ast.parse(expression, mode="eval").body)
            result.text = str(round(answer, 8) if isinstance(answer, float) else answer)
        except Exception:
            result.text = "Invalid calculation"

if __name__ == "__main__":
    TrustOS().run()
