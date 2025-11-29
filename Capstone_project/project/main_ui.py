import tkinter as tk
from tkinter import ttk
import cv2
import os
import threading
import sys
from PIL import Image, ImageTk
import time
from file_handling import file_handling
from image_generator import image_generator
import logging

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # setup logging 
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        
        #set up file handelr with base path for program
        self.base_path = self.get_base_path()
        self.file_handler = file_handling()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        #app configuration
        self.title("KWSA Parametric Drawing System")
        self.geometry("1100x700")
        self.configure(bg='#f0f0f0')
        
        # app icons
        icon = tk.PhotoImage(file=f"{self.base_path}/UI_images/kwsa-logo.png")
        self.iconphoto(True, icon)

        #styling of UI
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 12), background='#39a9e0', foreground='#1e4d93')
        self.style.configure('TLabel', font=('Arial', 12), background='#f0f0f0', foreground='#063045')
        self.style.configure('Header.TLabel', font=('Avenir', 24, 'bold'), background='#f0f0f0', foreground='#1e4d93')

        

        #create and pack main container for frames
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # storing reference to frames
        self.frames = {}
        for F in (HomePage, CustomSettingsPage, ProcessingPage, ImageSelectionPage, ExitPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def start_new_drawing(self):
        self.clean_up()
        self.frames[ProcessingPage].reset()
        self.show_frame(HomePage)


    def clean_up(self):
        # Delete temporary files and directories
        # Reset video path
        # Clear target and image paths
        self.file_handler.clean_up()

        # Reset frames that might have cached data
        for frame in self.frames.values():
            if hasattr(frame, 'reset'):
                frame.reset()

        self.logger.info("Cleanup completed. All temporary files and data have been removed.")

    def on_closing(self):
        self.logger.info("Window close button pressed. Cleaning up and exiting.")
        self.clean_up()
        self.quit()
        self.destroy()

    def clean_up(self):
        self.file_handler.clean_up()
        for frame in self.frames.values():
            if hasattr(frame, 'reset'):
                frame.reset()
        self.logger.info("Cleanup completed. All temporary files and data have been removed.")

    def get_base_path(self):
        """Get the base path for files and directories based on whether we are running from a script or a frozen executable."""
        if getattr(sys, 'frozen', False):  # If the script is compiled to an executable
            return os.path.dirname(sys.executable)
        else:  # If running in development (normal script)
            return os.path.dirname(os.path.abspath(__file__))    

    # display frame on screen
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # exit application after clean up
    def exit_application(self):
        self.logger.info("Closing app.")
        self.clean_up()
        self.quit()
        self.destroy()

    # start new drawing after clean up
    def start_new_drawing(self):
        self.logger.info("Starting new drawing.")
        self.clean_up()
        self.show_frame(HomePage)

    # override destroy method to ensure cleanup occurs
    def destroy(self):
        self.logger.info("Destroying object.")
        self.clean_up()
        super().destroy()

# home page class
class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.controller = controller
        self.base_path = self.get_base_path()
        
        # display title and subtitle
        title = ttk.Label(self, text="Key Word Sign Australia", style='Header.TLabel')
        title.pack(pady=(50, 20))

        subtitle = ttk.Label(self, text="Parametric Drawing System", font=('Arial', 18, 'bold'), foreground='#1e4d93')
        subtitle.pack(pady=(0, 30))

        instructions = ttk.Label(self, text="Please select an option to begin:", font=('Arial', 14))
        instructions.pack(pady=(0, 50))
        
        # buttons
        button_frame = ttk.Frame(self)
        button_frame.pack()

        # help button icon
        help_img = tk.PhotoImage(file=f"{self.base_path}/UI_images/help_logo.png")
        help_button = tk.Button(self, image=help_img, command=self.help_message)
        help_button.image = help_img  
        help_button.place(x=1000, y=20)

        # record video button
        record_button = ttk.Button(button_frame, text="Record Video", command=self.record_video, width=20)
        record_button.pack(side=tk.RIGHT, padx=20)

        # upload video button
        upload_button = ttk.Button(button_frame, text="Upload Video", command=self.upload_video, width=20)
        upload_button.pack(side=tk.LEFT, padx=20)

        
    
    def get_base_path(self):
        self.logger.info("Obtaining base path.")
        """Get the base path for files and directories based on whether we are running from a script or a frozen executable."""
        if getattr(sys, 'frozen', False):  # If the script is compiled to an executable
            return os.path.dirname(sys.executable)
        else:  # If running in development (normal script)
            return os.path.dirname(os.path.abspath(__file__))    


    def help_message(self):
        tk.messagebox.showinfo(message="To record a live video select Record button. For best results film in front of a plain background and keep videos to under 30 seconds")

    # handling video upload and moving ot the custom settings page
    def upload_video(self):
        self.logger.info("uploading video...")
        video_path = tk.filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
        if video_path:
            self.controller.video_path = video_path
            self.controller.show_frame(CustomSettingsPage)
            self.controller.frames[CustomSettingsPage].set_next_action('upload')

    # what to display on help button
    def help_message(self):
        tk.messagebox.showinfo("Help", "To record a live video, select the 'Record Video' button. For best results, film in front of a plain background and keep videos under 30 seconds.\n\nTo use an existing video, select the 'Upload Video' button.")

    # move to record_video page
    def record_video(self):
        self.logger.info("Navigating to CustomSettingsPage for recording.")
        self.controller.show_frame(CustomSettingsPage)
        self.controller.frames[CustomSettingsPage].set_next_action('record')
        
            

    
# class for custom user settings and UI
class CustomSettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        # init of page\setting and options
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.controller = controller
        self.next_action = None

        # title of page
        title = ttk.Label(self, text="Custom Settings", style='Header.TLabel')
        title.pack(pady=20)

        # page instructions
        instructions = ttk.Label(self, text="Adjust the settings below or use the defaults:", font=('Arial', 14))
        instructions.pack(pady=(0, 20))

        #frame for holding edge and blur settings
        settings_frame = ttk.Frame(self)
        settings_frame.pack(pady=20)
    
        # Edge Detection Settings
        edge_frame = ttk.LabelFrame(settings_frame, text="Edge Detection Settings")
        edge_frame.pack(side=tk.LEFT, padx=20, pady=10, fill="x")

        # radio button for edge detection settings
        self.edge_var = tk.StringVar(value="medium")
        ttk.Radiobutton(edge_frame, text="Weak", variable=self.edge_var, value="weak").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Radiobutton(edge_frame, text="Medium (Default)", variable=self.edge_var, value="medium").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Radiobutton(edge_frame, text="Strong", variable=self.edge_var, value="strong").pack(anchor=tk.W, padx=5, pady=2)
    
        # Blur Settings
        blur_frame = ttk.LabelFrame(settings_frame, text="Blur Filter Settings")
        blur_frame.pack(side=tk.LEFT, padx=20, pady=10, fill="x")

        # radio button for blur settings
        self.blur_var = tk.StringVar(value="weak")
        ttk.Radiobutton(blur_frame, text="Weak (Default)", variable=self.blur_var, value="weak").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Radiobutton(blur_frame, text="Medium", variable=self.blur_var, value="medium").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Radiobutton(blur_frame, text="Strong", variable=self.blur_var, value="strong").pack(anchor=tk.W, padx=5, pady=2)
    
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=30)
    
        ttk.Button(button_frame, text="Use Default Settings", command=self.use_default_settings).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Apply Custom Settings", command=self.apply_custom_settings).pack(side="left", padx=10)

    #set the next action the suer intends to perfomr
    def set_next_action(self, action):
        self.next_action = action

    #apply default settings
    def use_default_settings(self):
        self.proceed_with_action(edge_settings=(50, 150), blur_settings=(5,5))

    #Apply the users custom setting choices via radio buttons
    def apply_custom_settings(self):
        edge_settings = {
            "weak": (100, 200),
            "medium": (50, 150),
            "strong": (20, 100)
        }[self.edge_var.get()]
        
        blur_settings = {
            "weak": (5,5),
            "medium": (9,9),
            "strong": (15,15)
        }[self.blur_var.get()]

        # process user actions with settings
        self.proceed_with_action(edge_settings, blur_settings)

    #proceed to selection stage
    def proceed_with_action(self, edge_settings, blur_settings):
        self.logger.info("Processing user action choice...")
        if self.next_action == 'record':
            self.controller.frames[ProcessingPage].start_recording(edge_settings, blur_settings)
        elif self.next_action == 'upload':
            self.controller.frames[ProcessingPage].start_processing(edge_settings, blur_settings)
        self.controller.show_frame(ProcessingPage)
    

# class for processing images.
class ProcessingPage(ttk.Frame):
    def __init__(self, parent, controller):
        # init processing page 
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.controller = controller
        self.file_handler = file_handling()
        self.recording = False
        self.processing = False
        self.cap = None 

        #styling of page
        self.style = ttk.Style()
        self.style.configure('Processing.TFrame', background='#f0f0f0')
        self.style.configure('Blue.TLabel', foreground='#1e4d93', background='#f0f0f0', font=('Arial', 16, 'bold'))
        self.style.configure('ProcessingText.TLabel', foreground='#063045', background='#f0f0f0', font=('Arial', 14))
        
        #page title
        title = ttk.Label(self, text="Processing Your Video", style='Header.TLabel')
        title.pack(pady=(30, 10))

        #frame for displaying video preview during recording
        self.preview_frame = ttk.Frame(self, style='Processing.TFrame')
        self.preview_frame.pack(pady=20)
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack()

        #label for status messages
        self.message = tk.Label(self, text="Initializing...", font=('Arial', 20), fg='#063045')
        self.message.pack(pady=10)

        # frame progress bar
        self.progress_frame = ttk.Frame(self, style='Processing.TFrame')
        self.progress_frame.pack(pady=10, padx=50, fill='x')
        
        # percentage display
        self.progress = ttk.Progressbar(self.progress_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(fill='x')

        #label to display progress percent
        self.progress_percent = ttk.Label(self.progress_frame, text="0%", style='ProcessingText.TLabel')
        self.progress_percent.pack()

        # stop button 
        self.control_frame = ttk.Frame(self, style='Processing.TFrame')
        self.control_frame.pack(pady=20)
        self.stop_button = ttk.Button(self.control_frame, text="Stop Recording", command=self.stop_recording)
        self.cancel_button = ttk.Button(self.control_frame, text="Cancel", command=self.cancel_processing)
        self.cancel_button.pack(side='left', padx=10)
        
        self.stop_recording_flag = threading.Event()
        self.cancel_flag = threading.Event()
        self.edge_settings = (50, 150)  # Default edge settings
        self.blur_settings = (5, 5)  # Default blur settings
        self.recording_thread = None
        self.processing_thread = None

    # dialog for completion of processing
    def show_completion_dialog(self):
        self.logger.info("User images and svg generated.")
        result = tk.messagebox.askquestion("Processing Complete", 
                                    "Video processing is complete! Would you like to select images for conversion?",
                                    icon='info')
        if result == 'yes':
            self.controller.show_frame(ImageSelectionPage)
            self.controller.frames[ImageSelectionPage].load_images()
        else:
            self.controller.show_frame(HomePage)

    # start recoding video via opencv
    def start_recording(self, edge_settings=None, blur_settings=None):
        self.logger.info("User recording starting.")
        if edge_settings is not None:
            self.edge_settings = edge_settings
        if blur_settings is not None:
            self.blur_settings = blur_settings
        
        self.message.config(text="Recording video... Press 'Stop Recording' when finished")
        self.progress.config(mode="indeterminate")
        self.progress.start()
        self.stop_recording_flag.clear()
        self.cancel_flag.clear()
        
        self.stop_button.pack(side='left', padx=10)
        self.cancel_button.pack(side='left', padx=10)
        
        # Start recording in a separate thread
        self.recording_thread = threading.Thread(target=self.record_video, daemon=True)
        self.recording_thread.start()
    # start processing with provided settings
    def start_processing(self, edge_settings=None, blur_settings=None):
        self.logger.info("Begin video processing.")
        if edge_settings is not None:
            self.edge_settings = edge_settings
        if blur_settings is not None:
            self.blur_settings = blur_settings
        
        self.message.config(text="Processing your video... Please wait")
        self.progress.config(mode="determinate")
        self.progress["value"] = 0
        self.cancel_flag.clear()
        
        self.stop_button.pack_forget()
        self.cancel_button.pack(side='left', padx=10)
        
        self.processing_thread = threading.Thread(target=self.process_video, daemon=True)
        self.processing_thread.start()

    #record video
    def record_video(self):
        self.cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
        start_time = time.time()
        max_duration = 60  # 60 seconds max

        while not self.stop_recording_flag.is_set() and not self.cancel_flag.is_set():
            ret, frame = self.cap.read()
            if ret:
                out.write(frame)
                self.update_preview(frame)
                elapsed_time = int(time.time() - start_time)
                self.message.config(text=f"Recording video... Duration: {elapsed_time}s")
                self.update_progress(min(elapsed_time, max_duration), max_duration)
                if elapsed_time >= max_duration:
                    break
            else:
                break

        out.release()
        self.release_camera()

        if not self.cancel_flag.is_set():
            self.controller.video_path = 'output.avi'
            self.after(0, lambda: self.start_processing(self.edge_settings, self.blur_settings))
        else:
            self.after(0, self.return_to_home)

    def release_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        cv2.destroyAllWindows()

    #process with settings provided
    def process_video(self):
        try:
            video_path = self.controller.video_path
            lower, upper = self.edge_settings
            blur_Ksize = self.blur_settings

            self.message.config(text="Processing video...")
            self.update_progress(0, 60)  # 60 seconds max

            # Call the actual video processing function
            img_gen = image_generator(video_path)
            img_gen.image_extracting(max_frames=120, lower=lower, upper=upper, blur_Ksize=blur_Ksize, output_folder='extracted_frames', max_duration=60)
            
            self.file_handler = img_gen.file_handler  # Assign the file_handler from img_gen

            if self.cancel_flag.is_set():
                return

            self.message.config(text="Processing complete! Preparing image selection...")
            self.update_progress(60, 60)
            self.after(2000, self.show_image_selection)
        except Exception as e:
            self.after(0, lambda: tk.messagebox.showerror("Error", f"An error occurred during processing: {str(e)}"))
            self.after(0, lambda: self.controller.show_frame(HomePage))

    #display images selection page
    def show_image_selection(self):
        self.controller.show_frame(ImageSelectionPage)
        self.controller.frames[ImageSelectionPage].load_images()

    # update preview window with current frame during recording
    def update_preview(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (320, 240))
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.preview_label.config(image=photo)
        self.preview_label.image = photo

    #update progress bar percentage
    def update_progress(self, current, total):
        percentage = int((current / total) * 100)
        self.progress["value"] = percentage
        self.progress_percent.config(text=f"{percentage}%")
        self.update_idletasks()

    #end recording
    def stop_recording(self):
        self.stop_recording_flag.set()
        self.message.config(text="Stopping recording...")

    #end processing
    def cancel_processing(self):
        self.cancel_flag.set()
        self.message.config(text="Cancelling operation...")
        if self.recording_thread and self.recording_thread.is_alive():
            self.stop_recording_flag.set()
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=5)
        
        self.release_camera()

        if self.file_handler:
            self.file_handler.clean_up()

        self.after(1000, self.return_to_home)

    #return to home page after operations
    def return_to_home(self):
        self.logger.info("Returning to home.")
        self.controller.clean_up()
        self.controller.show_frame(HomePage)
        self.reset() 
        tk.messagebox.showinfo("Operation Cancelled", "The operation has been cancelled. You can start a new process from the home page.")

    def reset(self):
        self.release_camera()
        self.preview_label.config(image='')
        self.message.config(text="Initializing...")
        self.progress["value"] = 0
        self.progress_percent.config(text="0%")
        self.stop_recording_flag.clear()
        self.cancel_flag.clear()

# class for selection of previewed images to get svg
class ImageSelectionPage(ttk.Frame):
    def __init__(self, parent, controller):
        # init settings
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        #save reference to the controller
        self.controller = controller
        self.file_handler = None

        # title label
        self.title = ttk.Label(self, text="Select Images for Conversion", style='Header.TLabel')  
        self.title.pack(pady=20)

        # instructions guide for users
        self.instructions = ttk.Label(self, text="Choose the images you want to convert to SVG:", font=('Arial', 14))
        self.instructions.pack(pady=(0, 20))

        # create canvas widget for displaying images
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # scroll region 
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        #add the scrollable frame to canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # position the canvas and scroll bar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        #button for holding convert and cancel buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=20)

        # get associated svg file
        self.convert_button = ttk.Button(self.button_frame, text="Convert Selected", command=self.convert_selected)
        self.convert_button.pack(side=tk.LEFT, padx=10)

        #cancel selection and return to home
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.cancel_selection)
        self.cancel_button.pack(side=tk.LEFT, padx=10)

        #hold selected images
        self.image_vars = []

    def cancel_selection(self):
        self.logger.info("Canceling image selection and cleaning up.")
        if self.file_handler:
            self.file_handler.clean_up()
        self.controller.clean_up()  # This will clean up any remaining files
        self.controller.show_frame(HomePage)

    def reset(self):
        # Clear previous selections and images
        self.logger.info("Clearing selected images in file_handler.")
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_vars.clear()
        if self.file_handler:
            self.file_handler.clear_image_path()
            self.file_handler.clear_target_path()

    # rest page before loading new images
    def load_images(self):
        self.reset()
        self.logger.info("Start load images.")
        processing_page = self.controller.frames[ProcessingPage]
        if processing_page.file_handler is None:
            self.logger.error("No file handler available. Please process a video first.")
            tk.messagebox.showerror("Error", "No images to display. Please process a video first.")
            self.controller.show_frame(HomePage)
            return

        self.file_handler = processing_page.file_handler
        temp_dir = self.file_handler.get_temp_dir()
        images = [f for f in os.listdir(temp_dir) if f.endswith('.png')]
        
        # Calculate the number of columns based on the canvas width
        canvas_width = self.canvas.winfo_width()
        num_columns = max(1, canvas_width // 220)  # 220 = image width (200) + padding (20)

        for i, image_name in enumerate(images):
            image_path = os.path.join(temp_dir, image_name)
            img = Image.open(image_path)
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)
            
            var = tk.IntVar()
            self.image_vars.append(var)
            
            chk = ttk.Checkbutton(self.scrollable_frame, image=photo, variable=var)
            chk.image = photo
            chk.grid(row=i//num_columns, column=i%num_columns, padx=10, pady=10)

        # Update the scroll region after adding all images
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # handle the conversion of images and svg
    def convert_selected(self):
        self.logger.info("Start conversion.")
        selected_indices = [i for i, var in enumerate(self.image_vars) if var.get()]
        if not selected_indices:
            self.logger.warning("No images selected for conversion.")
            tk.messagebox.showinfo("No Selection", "Please select at least one image to convert.")
            return
    
        if self.file_handler is None:
            self.logger.error("No file handler available. Please process a video first.")
            tk.messagebox.showerror("Error", "No file handler available. Please process a video first.")
            self.controller.show_frame(HomePage)
            return

        try:
            self.file_handler.saved_target_name = [self.file_handler.image_paths[i] for i in selected_indices]
            self.file_handler.format_png_to_svg()
            self.file_handler.extract_export()
    
            self.logger.info(f"Converted {len(selected_indices)} images to SVG.")
            tk.messagebox.showinfo("Conversion Complete", f"Converted {len(selected_indices)} images to SVG.")
            self.controller.show_frame(ExitPage)
        except IndexError as e:
            self.logger.error(f"Index error during conversion: {str(e)}")
            tk.messagebox.showerror("Error", f"An error occurred during conversion: list index out of range. Please try processing the video again.")
            self.controller.show_frame(HomePage)
        except Exception as e:
            self.logger.error(f"Error during conversion: {str(e)}")
            tk.messagebox.showerror("Error", f"An error occurred during conversion: {str(e)}")
            self.controller.show_frame(HomePage)


class ExitPage(ttk.Frame):
    def __init__(self, parent, controller):
        # init exit page
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.controller = controller
        
        # page title
        title = tk.Label(self, text="Key Word Sign", font=('Avenir', 60), fg='#1e4d93')
        title.pack()
        subtitle = tk.Label(self, text="Australia", font=('Arial', 40, 'bold italic'), pady=10, fg='#1e4d93')
        subtitle.pack()

        #farewell message and subtitle
        farewell_message = tk.Label(self, text="Your Key Word Sign drawings are now converted to SVG and ready to use!", font=('Arial', 20), fg='#063045')
        farewell_message.pack(pady=20)

        # exit button to close app
        exit_button = tk.Button(self, text="Exit", font=('Arial', 40), bg='red', fg='#1e4d93', command=self.exit_application)
        exit_button.place(x=600, y=300)

        #start new drawing process button
        start_again_button = tk.Button(self, text="New Drawing", font=('Arial', 40), bg='#39a9e0', fg='#1e4d93', command=lambda: controller.start_new_drawing())
        start_again_button.place(x=200, y=300)

    def exit_application(self):
        self.logger.info("Exiting application and cleaning up.")
        self.controller.clean_up()
        self.controller.exit_application()

# main entry point for program
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()