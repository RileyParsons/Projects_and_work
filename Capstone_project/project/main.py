import cv2 as cv
from file_handling import file_handling
from image_generator import image_generator
import tkinter as tk
import os
import logging
import sys

# Set up the logging configuration to track events and errors
logging.basicConfig(
    filename='app_log.log',         # Log file name
    filemode='a',                   # Append mode to keep adding new logs
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format including timestamp, log level, and message
    level=logging.DEBUG             # Logging level (DEBUG captures everything)
)

# Function to record video using the default camera
def record_video():
    cap = cv.VideoCapture(0)  # Open default camera
    fourcc = cv.VideoWriter_fourcc(*'XVID')  # Define codec for video format
    out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))  # Create video writer object to save recording

    while True:
        ret, frame = cap.read()  # Read frame from the camera
        if ret:
            out.write(frame)  # Write the frame to the output file
            cv.imshow('Recording... Press Q to stop', frame)  # Display the recording
            if cv.waitKey(1) & 0xFF == ord('q'):  # Press 'Q' to stop recording
                break
        else:
            break

    cap.release()  # Release the camera
    out.release()  # Release the video writer
    cv.destroyAllWindows()  # Close all OpenCV windows
    return 'output.avi'  # Return the path of the saved video file

# Function to process a given video and generate SVG files based on frame extraction and edge detection
def process_video(video_path, lower=50, upper=150, blur_Ksize=(5, 5)):
    img_gen = image_generator(video_path)  # Create an instance of `image_generator` with the selected video

    print("Extracting frames from the video...")
    # Extract frames from the video and process each one
    img_gen.image_extracting(max_frames=120, lower=lower, upper=upper, blur_Ksize=blur_Ksize, output_folder='extracted_frames')
    print("Frame extraction complete.")
    
    print("Creating SVG files...")
    # Generate SVG files for each extracted frame
    for frame_path in img_gen.file_handler.get_image_paths():
        if os.path.exists(frame_path):
            frame = cv.imread(frame_path, cv.IMREAD_GRAYSCALE)  # Read the frame as a grayscale image
            if frame is not None:
                img_gen.tracer(frame)  # Trace the frame and create an SVG file
            else:
                print(f"Error: unable to read image: {frame_path}")
        else:
            print(f"Warning: Frame file not found: {frame_path}")
    
    # Handle exporting and cleaning up the files
    img_gen.file_handler.select_for_export()
    img_gen.file_handler.extract_export()
    
    img_gen.file_handler.clean_up()
    
    print("Processing complete.")
    return "Video processing completed successfully."

# Function to handle video upload through a file dialog
def handle_upload(video_path=None):
    if video_path is None:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_handler = file_handling()  # Create a file handling object
        video_path = file_handler.select_video_file()  # Open the file dialog to select a video
        root.destroy()
        del file_handler

    if video_path and os.path.exists(video_path):  # Check if a valid video file was selected
        print(f"Processing video: {video_path}")
        try:
            return process_video(video_path)  # Process the selected video
        except Exception as e:
            print(f"Error processing video: {e}")
            import traceback
            traceback.print_exc()
            return "Error occurred while processing the video."
    else:
        return "No valid video selected or file does not exist."

# Function to handle video recording and then process the recorded video
def handle_record():
    video_path = record_video()  # Record a new video using the camera
    return process_video(video_path)  # Process the recorded video

# Function to handle command-line interaction for video processing
def handle_cli():
    print("Welcome to the Video Processing Application")
    print("1. Upload a video")
    print("2. Record a video")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        return handle_upload()  # Handle video upload option
    elif choice == '2':
        return handle_record()  # Handle video recording option
    else:
        return "Invalid choice. Please select 1 or 2."

# Function to determine if custom processing settings should be used
def custom_mode():
    print("Please select settings")
    print("1. Default settings")
    print("2. Custom settings")

    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        return False
    elif choice == '2':
        return True
    else:
        return "Invalid choice. Please select 1 or 2."

# Function to set the strength of edge detection based on user selection
def edge_detection_settings():
    print("Edge Detection Filter Settings")
    print("1. Weak edge detection filter")
    print("2. Medium edge detection filter (Default)")
    print("3. Strong edge detection filter")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        return 100, 200  # Weak edge detection
    elif choice == '2':
        return 50, 150  # Medium edge detection (default)
    elif choice == '3':
        return 20, 100  # Strong edge detection
    else:
        return "Invalid choice. Please select 1, 2, or 3."

# Function to define the blur settings for image preprocessing
def blur_settings():
    print("Image Blur Filter Settings")
    print("1. Weak blur filter (Default)")
    print("2. Medium blur filter")
    print("3. Strong blur filter")

    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        return (5, 5)  # Weak blur (default)
    elif choice == '2':
        return (9, 9)  # Medium blur
    elif choice == '3':
        return (15, 15)  # Strong blur
    else:
        return "Invalid choice. Please select 1, 2, or 3."

# Main function to handle the overall workflow and user interactions
def main():
    try:
        logging.info("Program started")  # Log when the program starts
        while True:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            # Display menu options to the user
            print("Select an option:")
            print("1. Upload Video")
            print("2. Record Video")
            print("3. Open CLI")
            print("4. Quit")
            
            choice = input("Enter your choice (1, 2, 3, or 4): ")
            
            if choice == '1':
                result = handle_upload()  # Upload and process video
            elif choice == '2':
                result = handle_record()  # Record and process video
            elif choice == '3':
                result = handle_cli()  # Open the CLI interface
            elif choice == '4':
                print("Exiting program")
                break  # Exit the loop and terminate the program
            else:
                result = "Invalid choice."

            print(result)  # Display the result of the selected option
            root.destroy()  # Close the hidden root window
    except Exception as e:
        # Log the exception with a traceback for debugging
        logging.exception("An error occurred: %s", e)
        print(f"A crash occurred. Details have been logged.")
        sys.exit(1)  # Exit the program with an error status

if __name__ == "__main__":
    main()  # Run the main function when the script is executed
