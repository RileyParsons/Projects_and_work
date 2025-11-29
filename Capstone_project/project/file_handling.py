import cv2 as cv
import numpy as np
from datetime import date
from tkinter import Tk, filedialog
from pathlib import Path
import shutil
import sys
import logging
import os

# The `file_handling` class is used to manage files and directories 
# related to the project, such as videos, temporary images, and SVG files.
class file_handling:
    
    # Constructor to initialize file handling class and setup necessary directories
    def __init__(self, video=None):
        self.video_file_path = video  # Path to the video file
        self.base_path = self.get_base_path()  # Get the base path for the project

        # Define directories for SVG and temporary images
        self.svg_dir = Path(self.base_path) / "svg_images"
        self.temporary_dir = Path(self.base_path) / "temporary_images"

        # Initialize lists to track image paths and target names
        self.image_paths = []  
        self.saved_target_name = []

        # Create directories if they do not exist
        self.create_dir(self.svg_dir)
        self.create_dir(self.temporary_dir)

        # Setup logging for tracking events and errors
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    # Destructor to log when the object is destroyed
    def __del__(self):
        self.logger.info("File_handling object destroyed")

    # Returns the base path depending on whether the script is frozen into an executable
    def get_base_path(self):
        """Get the base path for files and directories based on 
        whether we are running from a script or a frozen executable."""
        if getattr(sys, 'frozen', False):  # If the script is compiled to an executable
            return os.path.dirname(sys.executable)
        else:  # If running in development (normal script)
            return os.path.dirname(os.path.abspath(__file__))

    # Create a directory at the specified path if it does not exist
    def create_dir(self, directory):
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            self.logger.error(f"Failed to create directory: {e}")

    # Clear and recreate a directory
    def clear_dir(self, directory):
        try:
            if Path(directory).exists():
                shutil.rmtree(directory)  # Remove the directory and its contents
                Path(directory).mkdir(parents=True, exist_ok=True)  # Recreate it
        except PermissionError as e:
            self.logger.error(f"Failed to delete directory {directory} : {e}")

    # Delete all temporary images
    def delete_all_temp(self):
        self.clear_dir(self.temporary_dir)

    # Delete all SVG images
    def delete_all_svg(self):
        self.clear_dir(self.svg_dir)

    # Clear the stored video path
    def clear_video_path(self):
        self.video_file_path = None

    # Clear the list of saved target names
    def clear_target_path(self):
        self.saved_target_name.clear()

    # Clear the list of image paths
    def clear_image_path(self):
        self.image_paths.clear()

    # Open a file dialog for the user to select a video file
    def select_video_file(self):
        #print("Opening file dialog...")
        try:
            # Open a dialog box for video file selection
            self.video_file_path = filedialog.askopenfilename(
                title="Select a video file",
                filetypes=[("Video files", "*.mp4 *.avi")]
            )
            # print(f"File dialog closed, selected path: {self.video_file_path}")
        except Exception as e:
            # print(f"Error during file selection: {e}")
            import traceback
            traceback.print_exc()

        if self.video_file_path:
            print(f"Video selected: {self.video_file_path}")
        else:
            print("No video selected.")

        return self.video_file_path

    # Open the selected video and apply settings for further processing
    def open_video(self):
        if not self.video_file_path:
            self.logger.warning("No video file selected.")
            return

        cap = cv.VideoCapture(self.video_file_path)  # Open the video file

        if not cap.isOpened():
            self.logger.error(f"Unable to open video file: {self.video_file_path}")
            return

        # Read and process each frame of the video
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                self.logger.error("Cannot receive frame")
                break

            # Convert the frame to grayscale and apply edge detection
            if frame is not None:
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                cv.imshow('Target Image', gray)

                # Apply Canny edge detection
                edge_lord = cv.Canny(gray, 50, 150)
                cv.imshow("Edge Detection", edge_lord)

                # Find and display contours on a blank image
                display_image = np.zeros((edge_lord.shape[0], edge_lord.shape[1], 4), dtype=np.uint8)
                contours, hierarchy = cv.findContours(edge_lord, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                cv.drawContours(display_image, contours, -1, (255, 255, 255, 255), 2)
                cv.imshow("Contours", display_image)

            if cv.waitKey(1) == ord('q'):  # Press 'q' to exit
                break

        cap.release()  # Release the video capture object
        cv.destroyAllWindows()  # Close all OpenCV windows

    # Get the video path
    def get_video_path(self):
        return self.video_file_path

    # Get the SVG directory path
    def get_svg_dir(self):
        return self.svg_dir

    # Get the temporary directory path
    def get_temp_dir(self):
        return self.temporary_dir

    # Get a copy of the image paths
    def get_image_paths(self):
        return self.image_paths

    # Get the paths of saved target images
    def get_target_images(self):
        return self.saved_target_name

    # once a user has selected a file to save this will keep track of its path
    def save_path(self, save_target):
        self.saved_target_name.append(save_target)    
    
    def add_to_temp(self, img):
        img_date = date.today()
    
        # Convert to a Path object to use glob
        temp_dir_path = Path(self.temporary_dir)
        
        # Find the next available image number
        img_number = len(list(temp_dir_path.glob(f'{img_date}_frame_*.png'))) + 1
        
        # Create the image path with the date and number in the filename
        image_path = temp_dir_path / f"{img_date}_frame_{img_number}.png"
        
        # Save the image and store the path
        try:
            cv.imwrite(str(image_path), img)
        except Exception as e:
            self.logger.error(f"Unable to save image in temp: {e}")
        self.image_paths.append(str(image_path))

    def add_to_svg(self):
        svg_date = date.today()
        svg_dir_path = Path(self.svg_dir)
        number = len(list(svg_dir_path.glob(f'{svg_date}_frame_*.svg'))) + 1

        return str(svg_dir_path / f"{svg_date}_frame_{number}.svg")



    # reset to default value
    def clear_video_path(self):
        self.video_file_path = None

    def clear_target_path(self):
        self.saved_target_name.clear()

    def clear_image_path(self):
        self.image_paths.clear()


    def clean_up(self):
        self.delete_all_temp()
        self.delete_all_svg()
        self.clear_video_path()
        self.clear_target_path()
        self.clear_image_path()


# foundation for svg_selection
    def select_for_export(self):
        root = Tk()
        root.withdraw()

        file_paths = filedialog.askopenfilenames(
            title=f"Select image files for export",
            filetypes=[("Image Files", "*.png")],
            initialdir=self.temporary_dir
        )

        self.saved_target_name.extend(file_paths)
        root.destroy()
        #reformat user selection
        self.format_png_to_svg()

    # change file name to match svg file
    def format_png_to_svg(self):
        self.saved_target_name = [
            Path(self.svg_dir) / Path(png_path).with_suffix('.svg').name
            for png_path in self.saved_target_name
        ]
        # print(f"Formatted SVG paths: {self.saved_target_name}")
        self.logger.info(f"Formatted SVG paths: {self.saved_target_name}")

    # for extracting and exporting to chosen directory for svg output
    def extract_export(self):
        root = Tk()
        root.withdraw()
        export_dir = filedialog.askdirectory(title="Select the target export directory")
        root.destroy()

        if not export_dir:
            self.logger.error("No directory selected")
            return

        today = date.today()
        folder = f"exported_svgs_{today}"
        export_path = Path(export_dir) / folder
        folder_number = 1
        while export_path.exists():
            export_path = Path(export_dir) / f"{folder}_{folder_number}"
            folder_number += 1
    
        export_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Created folder: {export_path}")
        self.logger.info(f"Number of files to export: {len(self.saved_target_name)}")
        self.logger.info(f"SVG directory: {self.svg_dir}")
        # print(f"Created folder: {export_path}")

        # print(f"Number of files to export: {len(self.saved_target_name)}")
        # print(f"SVG directory: {self.svg_dir}")


        for svg_file in self.saved_target_name:
            source_path = Path(svg_file)
            # print(f"Source path: {source_path}")
            # print(f"Attempting to copy: {source_path}")
            self.logger.info(f"Source path: {source_path}")
            self.logger.info(f"Attempting to copy: {source_path}")
            if source_path.exists():
                try:
                    shutil.copy(str(source_path), str(export_path / source_path.name))
                    self.logger.info(f"Successfully copied {source_path.name} to {export_path}")
                    #print(f"Successfully copied {source_path.name} to {export_path}")
                except Exception as e:
                    # print(f"Error copying {source_path.name}: {str(e)}")
                    self.logger.warning(f"Error copying {source_path.name}: {str(e)}")
            else:
                # print(f"File not found: {svg_file}")
                self.logger.warning(f"File not found: {svg_file}")

        # print("Export complete.")
        # print(f"Contents of export folder after copying:")
        self.logger.info("Export complete.")
        self.logger.info("Contents of export folder after copying:")
        for file in os.listdir(export_path):
            # print(f"  {file}")
            self.logger.info(f"{file}")
        # # Construct the corresponding SVG file name
        # svg_file = self.svg_dir / f"{base_name}.svg"

        # Check if the SVG file exists
        