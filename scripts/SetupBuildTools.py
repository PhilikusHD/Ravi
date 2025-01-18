import subprocess
import sys

from scripts.Utils import print_colored

class BuildToolsConfiguration:
    requiredCMakeVersion = "3.28"
    requiredNinjaVersion = "1.10.0"

    @classmethod
    def Validate(cls):
        cls.InstallBuildTools()

    @classmethod
    def CheckCMakeInstallation(cls):
        try:
            # Check CMake version
            cmake_version_output = subprocess.check_output(
                ["cmake", "--version"], text=True
            )
            cmake_version = cmake_version_output.strip().split()[2]

            if cmake_version >= cls.requiredCMakeVersion:
                print_colored(f"CMake {cmake_version} is installed.", 32)
                return True
            else:
                print_colored(
                    f"CMake {cls.requiredCMakeVersion} is required but version {cmake_version} is installed.",
                    31,
                )
                return False
        except FileNotFoundError:
            return False

    @classmethod
    def CheckNinjaInstallation(cls):
        try:
            # Check Ninja version
            ninja_version_output = subprocess.check_output(
                ["ninja", "--version"], text=True
            )
            ninja_version = ninja_version_output.strip()

            if ninja_version >= cls.requiredNinjaVersion:
                print_colored(f"Ninja {ninja_version} is installed.", 32)
                return True
            else:
                print_colored(
                    f"Ninja {cls.requiredNinjaVersion} is required but version {ninja_version} is installed.",
                    31,
                )
                return False
        except FileNotFoundError:
            return False

    @classmethod
    def InstallBuildTools(cls):
        permissionGranted = False
        isCMakeInstalled = cls.CheckCMakeInstallation()
        isNinjaInstalled = cls.CheckNinjaInstallation()
        if not isCMakeInstalled:
            while not permissionGranted:
                    print_colored(
                        f"CMake {cls.requiredCMakeVersion} is required but not installed. Please install it manually.",
                        31,
                    )
                    reply = (
                        input(
                        "Would you like to install CMake? [Y/N]: "
                        )
                        .lower()
                        .strip()[:1]
                    )
                    if reply == "n":
                        return

                    permissionGranted = reply == "y"
            

        if permissionGranted:
            if sys.platform.startswith("win"):
                cls.InstallCMakeOnWindows()
            elif sys.platform.startswith("linux"):
                cls.InstallCMakeOnLinux()
            else:
                print_colored(f"Platform '{sys.platform}' is not supported.", 31)

        permissionGranted = False
        if not isNinjaInstalled:
            while not permissionGranted:
                    reply = (
                        input(
                            "Would you like to install Ninja? [Y/N]: "
                        )
                        .lower()
                        .strip()[:1]
                    )
                    if reply == "n":
                        return

                    permissionGranted = reply == "y"

            if permissionGranted:
                if sys.platform.startswith("win"):
                    cls.InstallNinjaOnWindows()
                elif sys.platform.startswith("linux"):
                    cls.InstallNinjaOnLinux()
                else:
                    print_colored(f"Platform '{sys.platform}' is not supported.", 31)

    @classmethod
    def InstallCMakeOnWindows(cls):
        try:
            subprocess.run(
                ["winget", "install", "cmake"],
                check=True,
            )
            print_colored(
                f"CMake {cls.requiredCMakeVersion} has been installed successfully.", 32
            )
        except subprocess.CalledProcessError:
            print_colored(
                f"Failed to install CMake {cls.requiredCMakeVersion}. Please install it manually.",
                31,
            )

    @classmethod
    def InstallNinjaOnWindows(cls):
        try:
            subprocess.run(["winget", "install", "ninja-build.Ninja"], check=True)
            print_colored(
                f"Ninja {cls.requiredNinjaVersion} has been installed successfully.", 32
            )
        except subprocess.CalledProcessError:
            print_colored(
                f"Failed to install Ninja {cls.requiredNinjaVersion}. Please install it manually.",
                31,
            )

    @classmethod
    def InstallCMakeOnLinux(cls):
        package_managers = ["apt", "yum", "dnf", "zypper", "pacman"]
        installed_manager = None

        for manager in package_managers:
            try:
                subprocess.run(
                    [f"{manager}", "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                )
                installed_manager = manager
                break
            except FileNotFoundError:
                pass

        if installed_manager:
            try:
                subprocess.run(
                    [
                        f"sudo",
                        f"{installed_manager}",
                        "install",
                        f"cmake={cls.requiredCMakeVersion}",
                    ],
                    check=True,
                )
                print_colored(
                    f"CMake {cls.requiredCMakeVersion} has been installed successfully.",
                    32,
                )
            except subprocess.CalledProcessError:
                print_colored(
                    f"Failed to install CMake {cls.requiredCMakeVersion}. Please install it manually.",
                    31,
                )
        else:
            print_colored(
                "No suitable package manager found on your system. Please install CMake manually.",
                31,
            )

    @classmethod
    def InstallNinjaOnLinux(cls):
        package_managers = ["apt", "yum", "dnf", "zypper", "pacman"]
        installed_manager = None

        for manager in package_managers:
            try:
                subprocess.run(
                    [f"{manager}", "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                )
                installed_manager = manager
                break
            except FileNotFoundError:
                pass

        if installed_manager:
            try:
                subprocess.run(
                    [
                        f"sudo",
                        f"{installed_manager}",
                        "install",
                        f"ninja-build={cls.requiredNinjaVersion}",
                    ],
                    check=True,
                )
                print_colored(
                    f"Ninja {cls.requiredNinjaVersion} has been installed successfully.",
                    32,
                )
            except subprocess.CalledProcessError:
                print_colored(
                    f"Failed to install Ninja {cls.requiredNinjaVersion}. Please install it manually.",
                    31,
                )
        else:
            print_colored(
                "No suitable package manager found on your system. Please install Ninja manually.",
                31,
            )


# Main execution block
if __name__ == "__main__":
    # Validate the CMake and Ninja installation
    BuildToolsConfiguration.Validate()