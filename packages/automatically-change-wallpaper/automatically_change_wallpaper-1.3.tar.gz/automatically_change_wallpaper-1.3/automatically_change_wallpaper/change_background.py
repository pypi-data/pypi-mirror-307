import ctypes
from pathlib import Path

def set_wallpaper(img):

    if not Path(img).exists():
        print(f"Error: Video file '{img}' not found.")
        return

    # Set wallpaper using the temporary file path
    ctypes.windll.user32.SystemParametersInfoW(20, 0, img, 0)
    
