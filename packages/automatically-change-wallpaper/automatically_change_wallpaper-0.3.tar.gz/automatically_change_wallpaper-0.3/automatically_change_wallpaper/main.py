import sys 
import time
from pathlib import Path
from colorama import Fore, Style, init

import save_frame as sf
import change_background as cb

def main():

    init(autoreset=True)
    prints_file_path = Path('./output/prints.txt')
    base_path = Path('./output/data')
    status = Path('./assets/current.txt')
    
    def show_intro():
        print(Fore.CYAN + "-" * 60)
        print(Fore.GREEN + center_text("Video Wallpaper CLI Tool"))
        print(Fore.CYAN + "-" * 60)
        print(Fore.YELLOW + center_text("Welcome! This program allows you to:"))
        print(Fore.YELLOW + center_text("1. Capture frames from a video and save them as images."))
        print(Fore.YELLOW + center_text("2. Set your wallpaper to a frame from a video sequence."))
        print(Fore.YELLOW + center_text("Enjoy creating unique wallpapers from any video of your choice!"))
        print(Fore.CYAN + "-" * 60)
        time.sleep(2)  # Wait 2 seconds before showing the menu
    
    def MainMenu():
        print("\n" + Fore.CYAN + "-" * 60)
        print(Fore.GREEN + center_text("MAIN MENU"))
        print(Fore.CYAN + "-" * 60)
        print(Fore.MAGENTA + center_text("1 - Capture frames from video"))
        print(Fore.MAGENTA + center_text("2 - Change wallpaper to next frame"))
        print(Fore.MAGENTA + center_text("3 - Exit"))
        print(Fore.CYAN + "-" * 60)
    
    def capture_frames():
        video_path_input = input("Enter the path to the video file (press Enter to use default): ")
        video_path = Path(video_path_input) if video_path_input else Path('./assets/ArcaneSeason2.mp4')
        sf.screenshot(video_path)
    
    def Change():
        with open(status, 'r') as txt:
            chosen_frame = int(txt.read())
        chosen_frame += 1
        print(chosen_frame)
        img = Path(f"./output/data/frame{chosen_frame}.jpg").resolve()
        cb.set_wallpaper(str(img))
    
        with open(status, 'w') as txt:
            txt.write(str(chosen_frame))
    
    def center_text(text, width=60):
        return text.center(width)
    
    show_intro()
    
    while True:
    
        if len(sys.argv) > 1:
            if sys.argv[1].lower() == 'next':
                Change()
                break
    
        
        MainMenu()
        
        choice = input("Your option: ")
    
        if choice == "1":
            capture_frames()
    
        elif choice == "2":
            Change()
            input("Wallpaper changed. Press Enter to continue...")
    
    
        elif choice == "3":
            print("Exiting...")
            time.sleep(1)
            break
    
        else:
            print("Invalid option. Please try again.")
            time.sleep(1)
    
        
    
    
