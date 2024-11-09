class IconManager:
    def __init__(self, icon=None):
        self.icon = icon

    def set_icon(self, icon_path):
        self.icon = icon_path
        print(f"App icon set to {self.icon}")
