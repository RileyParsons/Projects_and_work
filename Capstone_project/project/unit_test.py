import unittest
from unittest import mock
from file_handling import file_handling
from image_generator import image_generator
import numpy as np


# https://docs.python.org/3/library/unittest.html
# https://docs.python.org/3/library/unittest.mock.html

# to run unit tests
# cd project
# python -m unittest unit_test.py

class TestFileHandling(unittest.TestCase):

    def setUp(self):
        self.handler = file_handling()

    # testing fundamentals

    # testing creating a directory
    def test_create_dir(self):
        self.assertTrue(self.handler.svg_dir.exists(), "SVG dir does not exists")
        self.assertTrue(self.handler.temporary_dir.exists(), "Temporary image dir does not exists")
        
    #deleting all temporary files
    def test_delete_all_temp(self):
        # fake file details
        file = self.handler.temporary_dir / "testing.png"
        # create a fake file
        file.touch()
        self.assertTrue(file.exists(), f"{file} does not exist")

        self.handler.delete_all_temp()
        self.assertFalse(file.exists(), f"{file} still exists within temp folder")

    # deleting all in svg fodler
    def test_delete_all_svg(self):
        # fake file details
        file = self.handler.svg_dir / "testing.png"
        # create a fake file
        file.touch()
        self.assertTrue(file.exists(), f"{file} does not exist")

        self.handler.delete_all_svg()
        self.assertFalse(file.exists(), f"{file} still exists within svg folder")

    #test video getting video path and clear
    def test_video_path(self):
        self.handler.video_file_path = "test_video.mp4"
        self.assertEqual(self.handler.get_video_path(), "test_video.mp4")

        self.handler.clear_video_path()
        self.assertIsNone(self.handler.get_video_path(), "Video path should be cleared")

    # adding to temporary dir test
    def test_add_to_temp(self):
        # fake image
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)  

        # Add the dummy image to the temporary directory
        self.handler.add_to_temp(dummy_image)
        
        # Verify that the image was added
        temp_files = list(self.handler.temporary_dir.glob("*.png"))
        self.assertEqual(len(temp_files), 1, "1 image should be added to the temp folder")

    # testing multiple images export
    def test_select_for_export(self):
        # Simulate selecting a few image files for export
        self.handler.saved_target_name = ["test_image_1.png", "test_image_2.png"]

        # Run the function that formats the image names to SVGs
        self.handler.format_png_to_svg()

        # Check that the names have been changed correctly
        expected_output = ["test_image_1.svg", "test_image_2.svg"]
        self.assertEqual(self.handler.saved_target_name, expected_output, "Image names should be converted to .svg")
    
    # testing clean up meothod for emptying directories
    def test_dir_clean_up(self):
            # Simulate adding paths
        self.handler.saved_target_name = ["dummy_image.svg"]
        self.handler.image_paths = ["dummy_image.png"]
        self.handler.video_file_path = "dummy_video.mp4"
        
        self.handler.clean_up()

        # Check if paths are cleared
        self.assertEqual(self.handler.saved_target_name, [], "Saved target names should be cleared")
        self.assertEqual(self.handler.image_paths, [], "Image paths should be cleared")
        self.assertIsNone(self.handler.video_file_path, "Video file path should be cleared")


    # testing error handling for a video that does not exist
    def test_opening_nonexisting_video(self):
        self.handler.video_file_path = "nonexistent_video.mp4"  # Set an invalid video path
        
        with self.assertLogs(level='INFO') as log:
            self.handler.open_video()
            self.assertIn("Unable to open video file: nonexistent_video.mp4", log.output[0], "Should log error about opening video file")
    
    #test failure to read video error logging
    def test_fail_to_read(self):
        self.handler.video_file_path = "valid_video.mp4"  # Set a video path
        
        # Mock the cv.VideoCapture object
        with mock.patch('cv2.VideoCapture') as MockVideoCapture:
            mock_cap = mock.MagicMock()
            MockVideoCapture.return_value = mock_cap
            mock_cap.isOpened.return_value = True  # Simulate that the video opens successfully
            mock_cap.read.side_effect = [(True, None), (False, None)]  # Simulate frame read fail

            with self.assertLogs(level='ERROR') as log:
                self.handler.open_video()

                # Assert the frame error is logged when frame reading fails
                self.assertIn("Cannot receive frame", log.output[-1], "Should log error about frame receiving")

    # test error in deleting file logging
    def test_file_deletion_error(self):
    # Simulate an error when deleting files
        # only testing one as deleiton code is the same
        with unittest.mock.patch('shutil.rmtree', side_effect=PermissionError("Permission denied")):
            with self.assertLogs(level='ERROR') as log:
                self.handler.delete_all_temp()
                directory = self.handler.get_temp_dir()
                self.assertIn(f"Failed to delete directory {directory} : Permission denied", log.output[-1], "Permission error should be logged")

    # test no extraction directory selection
    def test_no_extract_dir(self):
        with unittest.mock.patch('tkinter.filedialog.askdirectory', return_value=None): 
            with self.assertLogs(level='ERROR') as log:
                self.handler.extract_export()
                self.assertIn("No directory selected", log.output[-1], "should log an error for directory not being selected")

    # testing create directory error
    def test_create_dir_error(self):
            # Simulate a permission error when trying to create a directory
        with unittest.mock.patch('pathlib.Path.mkdir', side_effect=PermissionError("Cannot create directory")):
            with self.assertLogs(level='ERROR') as log:
                self.handler.create_dir(self.handler.svg_dir)
                self.assertIn("Failed to create directory: ", log.output[-1], "Directory creation error should be logged")

    # testing exporting invalid path
    def test_export_invalid_image_path(self):            
        # Set an invalid file in saved_target_name
        self.handler.saved_target_name = ["fake_image.svg"]
        with unittest.mock.patch('tkinter.filedialog.askdirectory', return_value="Home"): 
            with self.assertLogs(level='WARNING') as log:
                self.handler.extract_export()
                self.assertIn("File not found:", log.output[-1], "Missing file should log an error")

    # testing error in add to temp folder
    def test_add_to_temp_error(self):
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Simulate an error when writing the image to disk
        with unittest.mock.patch('cv2.imwrite', side_effect=Exception("Save failed")):
            with self.assertLogs(level='ERROR') as log:
                self.handler.add_to_temp(dummy_image)
                self.assertIn("Unable to save image in temp: Save failed", log.output[-1], "Error during image saving should be logged")

# less tests for this class as the core components of this class is in file_handling
class TestImageGenerator(unittest.TestCase):    
    def setUp(self):
        self.gen = image_generator("funny_video.mp4")

    # testing pre process handling error
    def test_pre_process_handling(self):
        with self.assertLogs(level="ERROR") as log:
            res = self.gen.pre_process(frame = "bad_frame_not_maltike_type", lower = 50, upper = 150, blur_Ksize=(5,5))
            self.assertIn(f"Invalid frame type not Matlike or ndarray", log.output[-1], "Error during logging should log a string.")
            self.assertIsNone(res, "Should result in None being returned from an invalid frame")

    # testing image extraction error handling
    def test_image_extracting_handling(self):
            with self.assertLogs(level="ERROR") as log:
                res = self.gen.image_extracting()
                self.assertIn("unable to access video:", log.output[0], "Should log error about unable to access video")
                self.assertIsNone(res, "Expected result to be None when video cannot be opened.")


