import cv2

def read_video(video_path):
    """
    Load a video file and return a list of frames from the video.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    # Read frames one by one
    while True:
        ret, frame = cap.read() # If ret is False, end of the stream (or encountered an error)
        if not ret:
            break
        frames.append(frame) # Store the frame one after the other
    cap.release()
    return frames

def save_video(ouput_video_frames,output_video_path):
    """
    Save a list of OpenCV / NumPy image frames to a video file.
    """
    # Choosing a codec. FOURCC is a 4-character code that specifies the video compression format.  
    # 'XVID' is a widely supported 'MPEG-4 Part 2' codec that works well for .avi containers.
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 

    #Create the VideoWriter object. , dedestination file, codec,  target frames, resoultion (width, height) 
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (ouput_video_frames[0].shape[1], ouput_video_frames[0].shape[0]))

    #Write each frame to the video file.
    for frame in ouput_video_frames:
        out.write(frame)
    # Release the writer to flush buffers 
    out.release()