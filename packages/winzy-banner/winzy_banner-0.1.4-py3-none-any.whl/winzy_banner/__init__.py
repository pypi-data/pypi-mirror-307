import winzy
import sys

import tkinter as tk

import customtkinter as ctk
import tkinter as tk


def display_banner(text):
    # Initialize the main window
    window = ctk.CTk()
    window.overrideredirect(True)  # Remove window borders for a cleaner look
    window.attributes("-topmost", True)  # Keep the banner on top
    window.attributes("-alpha", 0)  # Start with full transparency for fade-in effect

    # Focus the window to capture key events
    window.focus_force()

    # Set window title and appearance mode
    window.title(" ")
    ctk.set_appearance_mode("dark")  # Options: "dark", "light", "system"

    # Get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Set window size (90% width, 25% height of the screen)
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.25)
    window.geometry(f"{window_width}x{window_height}")

    # Calculate dynamic font size based on window size, capped for long text
    font_size = max(min(window_width // (len(text) // 2 + 1), window_height // 2), 20)

    # Create a frame for rounded corners
    frame = ctk.CTkFrame(window, corner_radius=20)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Create a label with the banner text
    banner_label = ctk.CTkLabel(
        frame, text=text, font=("Helvetica", font_size, "bold"), text_color="white"
    )
    banner_label.pack(expand=True, fill="both", padx=20, pady=20)

    # # Theme toggle button
    # def toggle_theme():
    #     current_mode = ctk.get_appearance_mode()
    #     new_mode = "light" if current_mode == "dark" else "dark"
    #     ctk.set_appearance_mode(new_mode)

    # theme_button = ctk.CTkButton(frame, text="Toggle Theme", command=toggle_theme)
    # theme_button.pack(pady=10)

    # # Close button
    # close_button = ctk.CTkButton(frame, text="Close", command=window.destroy)
    # close_button.pack(pady=10)

    # Function for smooth fade-in animation
    def fade_in():
        alpha = window.attributes("-alpha")
        if alpha < 1:
            alpha += 0.05
            window.attributes("-alpha", alpha)
            window.after(20, fade_in)

    # Define function to close the window on Escape key
    def close_window(event=None):
        window.destroy()

    # Bind the Escape key to close the window
    window.bind_all("<Escape>", close_window)

    # Start fade-in animation
    fade_in()

    # Enable dynamic resizing
    window.resizable(True, True)

    # Run the application loop
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
