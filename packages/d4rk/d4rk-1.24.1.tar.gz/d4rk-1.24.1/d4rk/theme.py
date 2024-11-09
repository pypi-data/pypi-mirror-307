class ThemeManager:
    def __init__(self, theme="dark"):
        self.theme = theme

    def set_theme(self, theme):
        self.theme = theme
        print(f"Theme set to {self.theme}")

    def enable_dark_mode(self):
        self.theme = "dark"
        print("Dark mode enabled.")

    def enable_light_mode(self):
        self.theme = "light"
        print("Light mode enabled.")
