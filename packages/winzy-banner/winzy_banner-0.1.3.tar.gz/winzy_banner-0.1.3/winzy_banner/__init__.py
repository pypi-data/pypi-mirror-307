import winzy
import sys

import tkinter as tk


def display_banner(text):
    window = tk.Tk()

    # Window Title
    window.title(" ")

    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Set window size
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.25)

    window.geometry(f"{window_width}x{window_height}")

    # Calculate font size based on window size
    font_size = min(window_width // len(text), window_height)

    # Create label with text as banner
    banner_label = tk.Label(window, text=text, font=("Helvetica", font_size))
    banner_label.pack(expand=True, fill="both")

    # Define function to close the window
    def close_window(event=None):
        window.destroy()

    # Bind the Escape key to close the window
    window.bind("<Escape>", close_window)

    window.mainloop()


# An example plugin implementation.


class HelloWorld:
    __name__ = "banner"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = subparser.add_parser("banner", description="Display Banner text")
        parser.add_argument(
            "text", nargs="*", help="The text to be displayed in the banner"
        )
        parser.set_defaults(func=self.hello)

    def hello(self, args):
        # this routine will be called when "winzy "banner is called."
        if args.text:
            display_banner(" ".join(args.text))
        else:
            text = sys.stdin.read()
            display_banner(" ".join(text))


banner_plugin = HelloWorld()
