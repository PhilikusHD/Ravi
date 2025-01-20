import os
import Utils

# Path to libtorch directory
libtorch_path = r"C:\AI\libtorch"

def check_and_download_libtorch():
    # Check if libtorch is installed
    if os.path.exists(libtorch_path):
        print(f"libtorch is already installed at {libtorch_path}.")
    else:
        print(f"libtorch is not installed at {libtorch_path}. Starting download...")
        # Replace with your download function (you already have this part)
        download_libtorch()

def download_libtorch():
    # Your existing code for downloading libtorch goes here
    # Example: 
    Utils.DownloadFile("https://download.pytorch.org/libtorch/nightly/cu126/libtorch-win-shared-with-deps-latest.zip")
    print("Downloading libtorch...")

# Run the check and download process
check_and_download_libtorch()
