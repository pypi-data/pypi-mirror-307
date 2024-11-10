import winzy_banner as w
from unittest import mock
import tkinter as tk
import customtkinter as ctk


@mock.patch("winzy_banner.ctk.CTkButton")
@mock.patch("winzy_banner.ctk.CTkLabel")
@mock.patch("winzy_banner.ctk.CTkFrame")
@mock.patch("winzy_banner.ctk.CTk")
def test_display_banner(mock_ctk, mock_frame, mock_label, mock_button):
    # Mock the window instance
    mock_window = mock.Mock()
    mock_ctk.return_value = mock_window

    # Set up mock for window size
    mock_window.winfo_screenwidth.return_value = 1920
    mock_window.winfo_screenheight.return_value = 1080

    # Set up mock return value for window attributes method
    mock_window.attributes.side_effect = (
        lambda *args: 0 if args[0] == "-alpha" else None
    )

    # Call the display_banner function
    w.display_banner("Hello World")

    # Assertions to check that the window was set up with correct dimensions
    window_width = int(1920 * 0.9)
    window_height = int(1080 * 0.25)
    mock_window.geometry.assert_called_once_with(f"{window_width}x{window_height}")

    # Assert the fade-in effect was initiated with transparency
    mock_window.attributes.assert_any_call("-alpha", 0)

    # Continue with other assertions as before
    mock_frame.assert_called_once_with(mock_window, corner_radius=20)
    font_size = max(
        min(window_width // (len("Hello World") // 2 + 1), window_height // 2), 20
    )
    mock_label.assert_called_once_with(
        mock_frame.return_value,
        text="Hello World",
        font=("Helvetica", font_size, "bold"),
        text_color="white",
    )
    mock_label.return_value.pack.assert_called_once_with(
        expand=True, fill="both", padx=20, pady=20
    )
    mock_window.bind_all.assert_called_once_with("<Escape>", mock.ANY)
    mock_window.resizable.assert_called_once_with(True, True)
    mock_window.mainloop.assert_called_once()
