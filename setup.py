from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base="Win32GUI")]

packages = ["idna", "PyQt5", "os", "sys", "random", "time", "threading"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "Main",
    options = options,
    version = "0.1",
    description = '',
    executables = executables
)