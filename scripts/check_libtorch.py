import os
import Utils

# Path to libtorch directory
libtorch_path = r"C:\\AI\\libtorch"
zip_path = r"C:\\AI\\libtorch-win-shared-with-deps-latest.zip"

def check_and_download_libtorch():
    # Check if libtorch is installed
    if os.path.exists(libtorch_path):
        print(f"libtorch is already installed at {libtorch_path}.")
    else:
        print(f"libtorch is not installed at {libtorch_path}. Starting download...")
        download_libtorch()

def download_libtorch():
    os.makedirs("C:\\AI")
    print("Downloading libtorch...")
    Utils.DownloadFile("https://download.pytorch.org/libtorch/nightly/cu126/libtorch-win-shared-with-deps-latest.zip", zip_path)
    print("Unzipping")
    Utils.UnzipFile(zip_path, False)

# Run the check and download process
check_and_download_libtorch()
