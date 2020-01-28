import sys
from cx_Freeze import setup, Executable
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}
# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
setup( name = "Backcalculation_app",
version = "0.1",
description = "SO2 volcanic emission calculator",
options = {"build_exe": build_exe_options},
executables = [Executable("run_file.py",'background_image.py','common_buttons.py','convert_to_csv.py','main_window.py',
                          'first_page.py','second_page.py','third_page.py','fourth_page.py','fifth_page.py',base=base)])