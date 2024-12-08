from cx_Freeze import setup, Executable
import sys
import os

# Ensure paths are correct for resources (icons, etc.)
icon_path = os.path.join(os.path.dirname(__file__), 'Assets', 'icons', 'OpenNoteLogo.ico')

# Include additional files (e.g., assets, styles, plugins)
build_exe_options = {
    "build_exe": "dist",
    "include_files": [
        "Styles",  
        "Assets",  
        "PluginWidgets",  
        "Saves",  
    ],
    "includes": [
        "cx_Freeze", "cx_Logging", "lief", #"MouseInfo"
         "numpy", #"opencv-python",
        "packaging", #"pillow",
        #"PyAutoGUI"
        #"PyGetWindow"
        #"PyMsgBox"
        "pyperclip",
        #"PyRect"
        #"PyScreeze"
        "PySide6",
        "pytweening", "shiboken6" 
    ],
    "packages": [
        "os", "sys", "json", "cv2", "numpy", "shiboken6", "PySide6",
        "PySide6.QtCore", "PySide6.QtGui", "PySide6.QtWidgets",
    ],
    "zip_include_packages": ["numpy", "opencv-python", "pillow", "PySide6"],  # Include large packages in the zip
    "zip_exclude_packages": ["PyQt5"],  
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

# Setup for the executable
setup(
    name="OpenNote",
    version="1.0.0", 
    description="An open source, extensible, cross-platform note-taking application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", 
                    base=base, 
                    target_name="OpenNote", 
                    icon=icon_path
                )],
)
