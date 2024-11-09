from .theme import ThemeManager
from .icon import IconManager
from .popup import PopupAd  # Import the PopupAd class

class D4RK:
    def __init__(self, theme="dark", icon=None):
        self.theme = ThemeManager(theme)
        self.icon = IconManager(icon)
        self.popup_ad = PopupAd()  # Initialize PopupAd

    def set_theme(self, theme):
        self.theme.set_theme(theme)

    def enable_dark_mode(self):
        self.theme.enable_dark_mode()

    def enable_light_mode(self):
        self.theme.enable_light_mode()

    def set_icon(self, icon_path):
        self.icon.set_icon(icon_path)

    def show_popup_ad(self, message, duration=5):
        """Show a popup ad with a custom message and duration."""
        self.popup_ad.set_message(message)
        self.popup_ad.set_duration(duration)
        self.popup_ad.show()

# Initialize framework
d4rk_app = D4RK(theme="dark")
