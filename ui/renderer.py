from rich.console import Console
from rich.text import Text

class Renderer:
    def __init__(self):
        self.console = Console()

    def render_out(self, text, justify):
        if justify == "left":
            self.console.print(text, justify="left")
        if justify == "center":
            self.console.print(text, justify="center")
        if justify == "full":
            self.console.print(text, justify="full")
        if justify == "right":
            self.console.print(text, justify="right")

    def render_input(self, prompt):
        centered_text = Text(prompt, justify="center")
        user_input = self.console.input(centered_text)
        return user_input