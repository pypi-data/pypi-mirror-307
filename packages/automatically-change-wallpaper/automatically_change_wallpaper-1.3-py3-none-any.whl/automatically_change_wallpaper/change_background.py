import ctypes
from pathlib import Path

def set_wallpaper(img):

    # check if the image file exists
    if not Path(img).exists():
        print(f"Error: Video file '{img}' not found.")
        return

    # Set the image as the desktop wallpaper using Windows API
    ctypes.windll.user32.SystemParametersInfoW(20, 0, img, 0)
    
