import winzy_banner as w
from unittest import mock
import tkinter as tk


@mock.patch("winzy_banner.tk.Tk")
@mock.patch("winzy_banner.tk.Label")
def test_display_banner(mock_label, mock_tk):
    # Mock the window instance
    mock_window = mock.Mock()
    mock_tk.return_value = mock_window

    # Set up mock for window size
    mock_window.winfo_screenwidth.return_value = 1920
    mock_window.winfo_screenheight.return_value = 1080

    # Call the display_banner function
    w.display_banner("Hello World")

    # Assertions to check that the window was set up with correct dimensions
    window_width = int(1920 * 0.9)
    window_height = int(1080 * 0.25)
    mock_window.geometry.assert_called_once_with(f"{window_width}x{window_height}")

    # Assert that the label was created with the correct text and font size
    font_size = min(window_width // len("Hello World"), window_height)
    mock_label.assert_called_once_with(
        mock_window, text="Hello World", font=("Helvetica", font_size)
    )

    # Assert that the label was packed with expand and fill options
    mock_label.return_value.pack.assert_called_once_with(expand=True, fill="both")

    # Assert that the mainloop was started
    mock_window.mainloop.assert_called_once()
