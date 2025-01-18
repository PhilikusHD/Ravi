import os
import subprocess
import sys
import re

import scripts.Utils as Utils
from scripts.Utils import print_colored

if sys.platform.startswith("win"):
    import winreg as reg

# Class for managing Clang configuration and validation

class ClangConfiguration:
    requiredClangVersion = "18.0.0"
    requiredClangdVersion = requiredClangVersion

    @classmethod
    def Validate(cls):
        if not cls.CheckClangInstallation():
            print_colored(
                "Clang is not installed or has an incompatible version. Engine needs clang >= 18.0.0", 31)
            cls.InstallClang()
        if not cls.CheckClangdInstallation():
            print_colored("Clangd is not installed or has an incompatible version. Engine needs clangd >= 18.0.0. Please ensure clangd has the same version as your installed compiler.", 31)
            cls.InstallClangd()

    @classmethod
    def CheckClangInstallation(cls):
        try:
            # Check Clang version
            output = subprocess.check_output(
                ["clang", "--version"], text=True)
            clang_version = output.strip().split()[2]

            match = re.search(r'InstalledDir:\s*(.*)', output)
            installation_dir = match.group(1).strip()

            if clang_version >= cls.requiredClangVersion:
                print_colored(
                    f"Clang {clang_version} is installed. ({installation_dir})", 32)
                return True
            print_colored(
                f"Clang {cls.requiredClangVersion} is required but version {clang_version} is installed.", 33)
            return False
        except FileNotFoundError:
            return False

    @classmethod
    def CheckClangdInstallation(cls):
        try:
            output = subprocess.check_output(
                ["clangd", "--version"], text=True)
            clangd_version = output.strip().split()[2]

            if clangd_version >= cls.requiredClangdVersion:
                print_colored(f"Clangd {clangd_version} is installed.", 32)
                return True

            print_colored(f"Clangd {cls.requiredClangdVersion} is required but version {clangd_version} is installed.", 33)
            return False
        except FileNotFoundError:
            return False

    @classmethod
    def InstallClangd(cls):
        permission_granted = False
        while not permission_granted:
            reply = input(
                f"Would you like to install Clangd {cls.requiredClangdVersion}? [Y/N]: ").lower().strip()[:1]
            if reply == 'n':
                return

            permission_granted = reply == 'y'

        if sys.platform.startswith("win"):
            msys2_path = "C:/msys64"
            clangd_command = f"{msys2_path}/usr/bin/bash -lc 'pacman -Sy --noconfirm mingw-w64-x86_64-clang-tools-extra"
            try:
                subprocess.run(clangd_command, shell=True, check=True)
                print_colored(
                    f"Clangd {cls.requiredClangdVersion} has been installed successfully.", 32)
            except subprocess.CalledProcessError:
                print_colored(
                    f"Failed to install Clang {cls.requiredClangdVersion}. Please install it manually (https://packages.msys2.org/packages/mingw-w64-x86_64-clang-tools-extra)", 31)

    @classmethod
    def InstallClang(cls):

        permission_granted = False
        while not permission_granted:
            reply = input(
                f"Would you like to install Clang {cls.requiredClangVersion}? [Y/N]: ").lower().strip()[:1]
            if reply == 'n':
                return

            permission_granted = reply == 'y'

        if sys.platform.startswith("win"):
            # Install MSYS2 if not already installed
            cls.InstallMSYS2()

            # Update MSYS2 key
            cls.UpdateMSYS2Keys()

            # Use MSYS2 to install Clang
            msys2_path = "C:/msys64"
            clang_command = f"{msys2_path}/usr/bin/bash -lc 'pacman -Sy --noconfirm mingw-w64-x86_64-clang'"

            try:
                subprocess.run(clang_command, shell=True, check=True)
                print_colored(
                    f"Clang {cls.requiredClangVersion} has been installed successfully.", 32)
            except subprocess.CalledProcessError:
                print_colored(
                    f"Failed to install Clang {cls.requiredClangVersion}. Please install it manually (https://packages.msys2.org/packages/mingw-w64-x86_64-clang)", 31)

            # Add the installed Clang to PATH on Windows
            clang_path = os.path.join(msys2_path, "mingw64", "bin")
            clang_lib = os.path.join(msys2_path, "mingw64", "lib")
            clang_include = os.path.join(msys2_path, "mingw64", "include")
            cls.SetEnvironmentVariable(clang_path)
            cls.SetEnvironmentVariable(clang_lib)
            cls.SetEnvironmentVariable(clang_include)

    @staticmethod
    def SetEnvironmentVariable(var_value, user=True):
        try:
            # Choose the registry key based on whether it's for user or system
            if user:
                reg_key = reg.HKEY_CURRENT_USER
                reg_path = r'Environment'
            else:
                reg_key = reg.HKEY_LOCAL_MACHINE
                reg_path = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'

            # Open the registry key for editing
            with reg.OpenKey(reg_key, reg_path, 0, reg.KEY_SET_VALUE | reg.KEY_QUERY_VALUE) as key:
                # Get the current value of the Path variable
                current_path, _ = reg.QueryValueEx(key, "Path")

                if var_value not in current_path:
                    # Append the new path to the current Path variable
                    updated_path = current_path + ';' + var_value

                    # Set the updated Path value
                    reg.SetValueEx(key, "Path", 0, reg.REG_EXPAND_SZ, updated_path)

                    print(f"Added '{var_value}' to Path successfully.")
                else:
                    print(f"'{var_value}' is already in the Path.")
            os.system('setx PATH "{}"'.format(updated_path))
    
        except Exception as e:
            print(f"Failed to update Path: {e}")


    @staticmethod
    def InstallMSYS2():
        # Download and install MSYS2
        msys2_installer = "https://github.com/msys2/msys2-installer/releases/download/2024-07-27/msys2-x86_64-20240727.exe"
        msys2_path = "C:/msys64"
        if not os.path.exists(msys2_path):
            # Download the MSYS2 installer to the current directory
            msys2_installer = "https://github.com/msys2/msys2-installer/releases/download/2024-07-27/msys2-x86_64-20240727.exe"
            msys2_installer_filename = os.path.basename(msys2_installer)
            msys2_installer_path = "Raven/vendor/" + msys2_installer_filename

            print("Downloading MSYS2 installer...")
            Utils.DownloadFile(msys2_installer, msys2_installer_path)

            # Run the installer
            print_colored("Running installer...", 36)
            os.system(os.path.abspath(msys2_installer_path))

            # Prompt the user to continue after the installer completes
            print_colored(
                input("Press Enter to continue after MSYS2 installation..."), 36)

            print_colored("MSYS2 installed successfully.", 32)
        else:
            print_colored("MSYS2 is already installed.", 32)

    @staticmethod
    def UpdateMSYS2Keys():
        msys2_path = "C:/msys64"
        try:
            subprocess.run(
                f"{msys2_path}/usr/bin/bash -lc 'pacman-key --init'", shell=True, check=True)
            subprocess.run(
                f"{msys2_path}/usr/bin/bash -lc 'pacman-key --refresh-keys'", shell=True, check=True)
            subprocess.run(
                f"{msys2_path}/usr/bin/bash -lc 'pacman -Syu'", shell=True, check=True)
        except subprocess.CalledProcessError:
            print_colored("Failed to run the necessary msys2 commands. Please open a bug report.", 31)


if __name__ == "__main__":
    ClangConfiguration.Validate()
