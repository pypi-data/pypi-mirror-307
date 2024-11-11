from pathlib import Path
import cv2
import os 
from PIL import Image
import numpy as np

def screenshot(video):
    
    # Check if the video file exists
    if not Path(video).exists():
        print(f"Error: Video file '{video}' not found.")
        return
    
    cam = cv2.VideoCapture(video)
    print(video)
    if not cam.isOpened():
        print("Error: Unable to open video.")
        exit()

    intvl = 3 #interval in seconds to capture frames
    fps = int(cam.get(cv2.CAP_PROP_FPS)) # Get the frames per second
    currentFrame = 0
    index = 0
    
    # Create the output directory if it doesn't exists
    try:
        if not os.path.exists(Path('./output/data')):
            os.makedirs(Path('./output/data'))
    
    except OSError:
        print('Error: Creating directory of data')
    
    print("fps: ", fps)
    
    while True:
        ret, frame = cam.read()
        if ret:
            # Capture frame at the specified interval
            if(currentFrame % (fps*intvl) == 0):
                name = Path(f'./output/data/frame{str(index)}.jpg')

                # Crop the image to remove the black bar
                #pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                #box = (0, 90, 1220, 630)
                #cropped_img = pil_img.crop(box)
                #cropped_frame = cv2.cvtColor(np.array(cropped_img), cv2.COLOR_RGB2BGR)
                
                # Save the caputured frame
                cv2.imwrite(name, cropped_frame)
                print(f"Capturing frames from {name} every {intvl} frames...")


                index += 1
            currentFrame += 1
    
        else:
            break
    
    cam.release()
    cv2.destroyAllWindows()



