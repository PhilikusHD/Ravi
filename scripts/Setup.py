import os
import platform

def Validate():
    from scripts.SetupPython import PythonConfiguration as PythonRequirements
    # Make sure everything we need for the setup is installed
    PythonRequirements.Validate()

    from scripts.SetupBuildTools import BuildToolsConfiguration as BuildRequirements
    # Make sure CMake and Ninja are insalled correctly
    BuildRequirements.Validate()

    from scripts.SetupClang import ClangConfiguration as ClangRequirements
    # Make sure Clang is installed correctly
    ClangRequirements.Validate()

    os.chdir("./../")
