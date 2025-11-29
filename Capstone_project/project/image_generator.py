import cv2 as cv
import numpy as np
import file_handling as fh
import svgwrite
import logging
import time
import cv2

# The `image_generator` class is responsible for extracting images from videos,
# processing them, and generating SVG files based on detected contours.
class image_generator:
    
    # Constructor to initialize the `image_generator` class
    def __init__(self, video):
        # Instantiate a file handling object for managing video and image paths
        self.file_handler = fh.file_handling(video)
        
        # Setup logging for tracking and debugging purposes
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        # Default values for edge detection and blurring.
        # These values might need to be adjusted depending on the specific requirements.
        # Edge detection may be integrated as part of the image extractor later.

    # Function to invert colors of a given image using bitwise operations
    def invert_colors(self, image):
        return cv.bitwise_not(image)

    # Preprocesses each frame by converting to grayscale, applying Gaussian blur, and detecting edges
    def pre_process(self, frame, lower, upper, blur_Ksize):
        try:    
            # Check if the frame is a valid numpy array
            if not isinstance(frame, np.ndarray):
                raise ValueError(f"Invalid frame type not Matlike or ndarray")
            
            # Convert the frame to grayscale
            grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv.GaussianBlur(grey, blur_Ksize, 0)
            
            # Use Canny edge detection with provided thresholds
            filter_frame = cv.Canny(blurred, lower, upper)
        
            # Invert the colors of the detected edges
            inverted_frame = self.invert_colors(filter_frame)
        
        except ValueError as e:
            self.logger.error(f"Invalid frame type: {e}")
            return None

        return inverted_frame

    # Extracts images from the video at specific intervals based on frame rate and duration
    def image_extracting(self, max_frames=60, output_folder='extracted_frames', lower=50, upper=150, blur_Ksize=(5,5), max_duration=60):
        try:
            # Get the path to the selected video file
            video_path = self.file_handler.get_video_path()
            
            # Open the video file using OpenCV
            video = cv2.VideoCapture(video_path)
            if not video.isOpened():
                raise PermissionError(f"Unable to open video.")
        
        except PermissionError as e:
            self.logger.error(f"unable to access video: {e}")
            return 
            
        # Get the frames per second (FPS) of the video
        fps = video.get(cv2.CAP_PROP_FPS)
        
        # Define the interval at which frames will be extracted (e.g., every half second)
        interval = int(fps / 2)
        frame_num = 0
        extracted_frames = 0
        start_time = time.time()

        # Loop to extract frames until reaching the max frames or duration limit
        while extracted_frames < max_frames:
            success, frame = video.read()
            if not success:
                break

            # Extract frame at specific intervals
            if frame_num % interval == 0:
                # Preprocess the frame for edge detection
                processed_frame = self.pre_process(frame, upper, lower, blur_Ksize)
                
                # Add the processed frame to the temporary directory
                self.file_handler.add_to_temp(processed_frame)
                
                # Trace the contours and generate the SVG file
                self.tracer(processed_frame)
                extracted_frames += 1

            frame_num += 1

            # Break if the maximum duration is exceeded
            if time.time() - start_time > max_duration:
                break

        # Release the video capture object and log the extraction result
        video.release()
        self.logger.info(f"Extracted {extracted_frames} frames to {output_folder}")

    # Trace the contours in the pre-processed frame and generate an SVG file
    def tracer(self, processed_frame):
        # Create a blank image canvas with the same size as the processed frame
        display_image = np.zeros((processed_frame.shape[0], processed_frame.shape[1], 4), dtype=np.uint8)
        
        # Find contours in the processed frame using the chain approximation method
        contours, hierarchy = cv.findContours(processed_frame, cv.CHAIN_APPROX_SIMPLE, cv.CHAIN_APPROX_TC89_KCOS)
    
        # Fill the canvas with a white background
        display_image.fill(255)
        
        # Draw the detected contours on the canvas with black color
        cv.drawContours(display_image, contours, -1, (0, 0, 0, 255), 2)
    
        # Retrieve the path for the SVG file
        svg_file_path = self.file_handler.add_to_svg()        
        
        # Create an SVG drawing object using `svgwrite`
        dwg = svgwrite.Drawing(svg_file_path, profile='full')
    
        # Add a white background rectangle to the SVG
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))
    
        # Loop through the contours and add polylines to the SVG file
        for c in contours:
            # Convert each contour to a list of coordinates and add to SVG as polylines
            points = c[:, 0, :].tolist()
            dwg.add(dwg.polyline(points, stroke=svgwrite.rgb(0, 0, 0), fill='none', stroke_width=2))
    
        # Log and save the SVG file
        self.logger.info(f"Saving SVG file to: {svg_file_path}")
        dwg.save()
        self.logger.info(f"SVG file saved successfully: {svg_file_path}")
