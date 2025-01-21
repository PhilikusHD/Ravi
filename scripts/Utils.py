import os
import sys
import time
import urllib
import urllib.request
from urllib.request import urlopen, urlretrieve

from zipfile import ZipFile

# Print colored text


def print_colored(text, color_code):
    print(f"\x1b[{color_code}m{text}\x1b[0m")


# Function to retrieve a system environment variable on Windows


def GetSystemEnvironmentVariable(name):
    if sys.platform.startswith("win"):
        import winreg

        try:
            # Open the Windows registry key for system environment variables
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"System\CurrentControlSet\Control\Session Manager\Environment",
            )
            # Query the value associated with the given name
            value, _ = winreg.QueryValueEx(key, name)
            return value
        except FileNotFoundError:
            # If the registry key is not found, return None
            return None
        except:
            # If an error occurs during retrieval, print an error message and return None
            print(f"Error retrieving system environment variable: {name}")
            return None
    else:
        # If not running on Windows, print a message and return None
        print("GetSystemEnvironmentVariable is only available on Windows")
        return None


# Function to retrieve a user environment variable on Windows


def GetUserEnvironmentVariable(name):
    if sys.platform.startswith("win"):
        try:
            # Open the Windows registry key for user environment variables
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
            # Query the value associated with the given name
            value, _ = winreg.QueryValueEx(key, name)
            return value
        except FileNotFoundError:
            # If the registry key is not found, return None
            return None
        except:
            # If an error occurs during retrieval, print an error message and return None
            print(f"Error retrieving user environment variable: {name}")
            return None
    else:
        # If not running on Windows, print a message and return None
        print("GetSystemEnvironmentVariable is only available on Windows")
        return None


# Function to download a file from the given URL and save it to the specified filepath


def DownloadFile(url, filepath):
    path = filepath
    filepath = os.path.abspath(filepath)
    print(filepath)
    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Handle the case when multiple URLs are provided as a list
    if type(url) is list:
        for url_option in url:
            print("Downloading", url_option, "to: ", filepath)
            try:
                # Recursively call DownloadFile for each URL in the list
                DownloadFile(url_option, filepath)
                return
            except Exception as e:
                # If an error occurs during download, print an error message, remove the downloaded file, and continue
                print(f"Error encountered: {e}. Proceeding with backup...\n\n")
                os.remove(filepath)
                pass
        # If none of the URLs in the list are successfully downloaded, raise an exception
        raise ValueError(f"Failed to download {filepath}")

    if not type(url) is str:
        raise TypeError("Argument 'url' must be of type list or string")

    # Function to display a progress bar during the download
    def report_hook(blocknum, blocksize, totalsize):
        downloaded = blocknum * blocksize
        percentage = min(downloaded / totalsize * 100, 100)
        sys.stdout.write(
            "\r[{}{}] {:.2f}%     ".format(
                "█" * int(50 * percentage / 100),
                "." * int(50 * (1 - percentage / 100)),
                percentage,
            )
        )
        sys.stdout.flush()

    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-Agent", "Mozilla/5.0")]
        urllib.request.install_opener(opener)
        print("Downloading", url)
        # Download the file from the URL and display a progress bar using the report_hook function
        urlretrieve(url, filename=filepath, reporthook=report_hook)
    except Exception as e:
        # If an error occurs during download, print an error message, remove the downloaded file, and raise the exception
        print(f"\nError encountered: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        raise

    sys.stdout.write("\n")


# Function to unzip a file


def UnzipFile(filepath, deleteZipFile=True):
    zipFilePath = os.path.abspath(filepath)  # get full path of files
    zipFileLocation = os.path.dirname(zipFilePath)

    zipFileContent = dict()
    zipFileContentSize = 0
    with ZipFile(zipFilePath, "r") as zipFileFolder:
        for name in zipFileFolder.namelist():
            zipFileContent[name] = zipFileFolder.getinfo(name).file_size
        zipFileContentSize = sum(zipFileContent.values())
        extractedContentSize = 0
        startTime = time.time()
        for zippedFileName, zippedFileSize in zipFileContent.items():
            UnzippedFilePath = os.path.abspath(f"{zipFileLocation}/{zippedFileName}")
            os.makedirs(os.path.dirname(UnzippedFilePath), exist_ok=True)
            if os.path.isfile(UnzippedFilePath):
                zipFileContentSize -= zippedFileSize
            else:
                zipFileFolder.extract(zippedFileName, path=zipFileLocation, pwd=None)
                extractedContentSize += zippedFileSize
            try:
                done = int(50 * extractedContentSize / zipFileContentSize)
                percentage = (extractedContentSize / zipFileContentSize) * 100
            except ZeroDivisionError:
                done = 50
                percentage = 100
            elapsedTime = time.time() - startTime
            try:
                avgKBPerSecond = (extractedContentSize / 1024) / elapsedTime
            except ZeroDivisionError:
                avgKBPerSecond = 0.0
            avgSpeedString = "{:.2f} KB/s".format(avgKBPerSecond)
            if avgKBPerSecond > 1024:
                avgMBPerSecond = avgKBPerSecond / 1024
                avgSpeedString = "{:.2f} MB/s".format(avgMBPerSecond)
            sys.stdout.write(
                "\r[{}{}] {:.2f}% ({})     ".format(
                    "█" * done, "." * (50 - done), percentage, avgSpeedString
                )
            )
            sys.stdout.flush()
    sys.stdout.write("\n")

    if deleteZipFile:
        os.remove(zipFilePath)  # delete zip file


def CompareVersions(v1, v2):
    """
    Compare two version strings v1 and v2.
    Returns:
        -1 if v1 < v2
         0 if v1 == v2
         1 if v1 > v2
    """
    v1_parts = [int(part) for part in v1.split(".")]
    v2_parts = [int(part) for part in v2.split(".")]

    for part1, part2 in zip(v1_parts, v2_parts):
        if part1 < part2:
            return -1
        elif part1 > part2:
            return 1

    if len(v1_parts) < len(v2_parts):
        return -1
    elif len(v1_parts) > len(v2_parts):
        return 1

    return 0