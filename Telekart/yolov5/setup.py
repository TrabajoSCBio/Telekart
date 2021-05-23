from cx_Freeze import setup,Executable
setup(
    name="RedNeuronal",
    version=0.1,
    description="project_description",
    executables=[Executable("launcher.py",base="Win32GUI")],
)