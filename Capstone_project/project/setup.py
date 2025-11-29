# requirements
# pip install cx_Freeze

#Virtual environment used to compile program
# Package            Version
# ------------------ ---------
# cx_Freeze          7.2.3
# cx_Logging         3.2.0
# importlib_metadata 8.5.0
# lief               0.15.1
# numpy              2.0.2
# opencv-python      4.10.0.84
# packaging          24.1
# pillow             10.4.0
# svgwrite           1.4.3
# tk                 0.1.0
# tomli              2.0.2
# typing_extensions  4.12.2
# zipp               3.20.2


# refernece documents
# https://cx-freeze.readthedocs.io/en/stable/setup_script.html

# script tells cx_freeze how to build the project

from cx_Freeze import setup, Executable
import sys
sys.setrecursionlimit(2000)


#dependencies are autimaticly detected but can be fine tuned here

# to invoke script: python setup.py build
build_exe_options = {
    "include_files": [("svg_images/", "svg_images/"), 
                      ("temporary_images/", "temporary_images/"),
                      ("UI_images/", "UI_images/"),
                      "file_handling.py",
                      "image_generator.py",
                      ],
                      
    "includes": ["os", "cv2", "numpy", "tkinter", "datetime", "svgwrite", "pathlib", "shutil", "logging", "sys", "time", "threading"],
    "excludes": ["email"]
}

#define main executable file


setup( name = 'KWSDS_console', 
      version = '1.1.0', 
      description = 'Swinburne student Key Word Sign Drawing System program.', 
      options={'build_exe': build_exe_options},
       executables = [Executable("main_ui.py", 
                                 base= "Win32GUI"
                                 )]
       #use all ptython versions from 3.9 up to but not including 3.13
       )

# to execute and compile

# computer does not need python installed on it to run th program
# python setup.py build