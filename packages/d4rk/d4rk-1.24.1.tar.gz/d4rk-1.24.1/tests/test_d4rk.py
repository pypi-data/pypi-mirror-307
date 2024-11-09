import unittest
from d4rk import D4RK
import time

class TestD4RK(unittest.TestCase):

    def test_set_theme(self):
        app = D4RK(theme="light")
        self.assertEqual(app.theme.theme, "light")

    def test_enable_dark_mode(self):
        app = D4RK()
        app.enable_dark_mode()  # Should print "Dark mode enabled."

    def test_set_icon(self):
        app = D4RK()
        app.set_icon("assets/default_icon.png")  # Should print "App icon set to assets/default_icon.png"
    
    def test_enable_light_mode(self):
        app = D4RK(theme="light")
        app.enable_light_mode()  # Should print "Light mode enabled."

    def test_popup_ad(self):
        app = D4RK()
        app.show_popup_ad("Buy our product now!", 3)  # Should display the message and auto-close after 3 seconds
        time.sleep(4)  # Wait for the ad to close
        app.show_popup_ad("Limited time offer!", 2)  # Another popup with a different message
        time.sleep(3)  # Wait for the ad to close

if __name__ == "__main__":
    unittest.main()
