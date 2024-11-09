import time
import threading

class PopupAd:
    def __init__(self, message="This is an ad!", display_duration=5):
        self.message = message  # The message to display
        self.display_duration = display_duration  # Time in seconds the ad will be shown
        self.is_shown = False  # State to track if the ad is displayed

    def _close_popup(self):
        """Close the popup after a set duration."""
        time.sleep(self.display_duration)
        self.is_shown = False
        print("Popup ad closed.")

    def show(self):
        """Display the popup ad with the message."""
        if not self.is_shown:
            self.is_shown = True
            print(f"Popup Ad: {self.message}")
            # Start a separate thread to close the ad after the display duration
            threading.Thread(target=self._close_popup).start()

    def set_message(self, message):
        """Change the popup message."""
        self.message = message

    def set_duration(self, duration):
        """Set the duration (in seconds) the popup will stay visible."""
        self.display_duration = duration
