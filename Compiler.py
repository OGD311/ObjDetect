from cx_Freeze import setup, Executable

# from os.path import expanduser
# import os.path
# import random

# home = expanduser("~")
# dir = os.path.join(home, rf"Documents\Euro Truck Simulator 2\online\billboards_cache\billboards_img\Billboard_img\Generated\build\Icons")
# files = os.listdir(dir)
# icons = rf"{random.choice(files)}"
# dir = os.path.join(dir,icons)


base = None    
icon = None
executables = [Executable("Object detection (YOLO4Mini Better).py",icon=icon, base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

build_exe_options = {
    "excludes": ["tkinter", "unittest"],
    "zip_include_packages": ["encodings", "PySide6","cvlib","cv2","mss","PIL"],
}


setup(
    name = "Object Detection",
    options=options,
    version = "1.0",
    description = 'Object Detection using cvlib and MSS',
    executables = executables
)


#run 'python Compiler.py build' from cmd prompt (no admin needed) with cd address being main folder of file to compile (Cmpiler.py needs to be in same folder also)