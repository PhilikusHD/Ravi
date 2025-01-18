from datetime import datetime
import os
import sys
import re
import subprocess
import shutil
import time
import argparse
import multiprocessing

from scripts.Utils import print_colored
from scripts import Setup
from scripts import Analyzer
import scripts.Cleanup as Cleaner

############### Coloring ###############
#   - Cyan - Info                      #
#   - Green - Success                  #
#   - Yellow - Warn                    # 
#   - Red - Error                      #
#   - Blue - Process                   #
########################################

# Constants
BUILD_TYPES = {"Debug", "Release"}
DEFAULT_BUILD_TYPE = "Release"
DEFAULT_JOBS = multiprocessing.cpu_count()
CLEAN_TYPES = {"all", "build"}
cwd = os.getcwd()


def setup_check():
    """
    Checks whether setup.py has been run before on the machine.
    If not, performs the initial setup process.
    """
    os.chdir(os.path.join(cwd, "scripts"))
    Setup.Validate()

def configure_project(build_type, build_dir, jobs, verbose, dry_run):
    """
    Configures Raven using CMake based on the chosen build type and build directory.
    """
    # Create the build directory if it doesn't exist and it's not the current directory
    if build_dir != cwd:
        if not os.path.exists(build_dir):
            print_colored(f"Creating build directory: {build_dir}", 36)
            os.makedirs(build_dir)

    # Change to the build directory
    os.chdir(build_dir)
    # Set the CMake command based on the build directory
    cmake_cmd = (
        f'cmake -G "Ninja" -DCMAKE_BUILD_TYPE={build_type} ..'
        if build_dir != cwd
        else f'cmake -G "Ninja" -DCMAKE_BUILD_TYPE={build_type} .'
    )

    result = subprocess.run(cmake_cmd, shell=True)
    if result.returncode != 0:
        print_colored("CMake configuration failed!", 31)
        sys.exit(1)

    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Project configured for {build_type}.", 32)

    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Starting compilation.", 34)
    success = compile_project(jobs, verbose, dry_run=dry_run)
    os.chdir(cwd)
    return success

def compile_project(jobs, verbose=False, output_file="Compilation.log", dry_run=False):
    """
    Compiles the project using Ninja with the specified number of jobs and writes the output to a file.
    If dry_run is True, it simulates the compilation process without actually running Ninja.
    """
    if dry_run:
        print_colored("Dry run: Skipping actual compilation.", 33)
        return True  # Simulate a successful dry run

    print_colored("Compiling...", 36)

    if verbose:
        os.system(f"ninja -j {jobs}")
        print_colored("Compilation completed without analyzer.", 32)
        return True  # Assume success if analyzer is disabled

    progress_width = 50
    progress_regex = r"\[(\d+)/(\d+)\]"
    total_targets = 0
    current_target = 0
    output_buffer = ""

    # Open Ninja process
    process = subprocess.Popen(
        f"ninja -j {jobs}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    try:
        with open(output_file, "w") as f:
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"{timestamp} - {output}")
                    f.flush()

                    match = re.search(progress_regex, output)
                    if match:
                        current_target, total_targets = map(int, match.groups())
                    progress_percent = (
                        (current_target / total_targets) * 100 if total_targets > 0 else 0
                    )
                    progress_chars = int(progress_width * progress_percent / 100)
                    progress_bar = (
                        "["
                        + "#" * progress_chars
                        + " " * (progress_width - progress_chars)
                        + "]"
                    )
                    sys.stdout.write(f"\r{progress_bar} {progress_percent:.2f}% ")
                    sys.stdout.flush()

                    output_buffer += output

            sys.stdout.write("\n")
            sys.stdout.flush()

            # Handle remaining output
            output_remainder, _ = process.communicate()
            if output_remainder:
                f.write(output_remainder)
                f.flush()
                output_buffer += output_remainder

    except Exception as e:
        print_colored(f"Error during compilation: {str(e)}", 31)
        process.terminate()
        sys.exit(1)

    finally:
        process.stdout.close()
        process.stderr.close()
        process.wait()

    # Analyze the output
    analysis_result = Analyzer.analyze_output(output_buffer)
    if not analysis_result[0] and not analysis_result[2]:
        print_colored("Compilation succeeded with no critical warnings or errors.", 32)
        return True
    else:
        print_colored("Compilation failed or had critical warnings.", 31)
        return False

def main():
    """
    Linter says I need a docstring, I follow linter...
    except for when it says "Line too long"
    """
    build_start = time.time()

    # Argument parsing
    parser = argparse.ArgumentParser(description="Script for compiling Raven")
    parser.add_argument(
        "build_type",
        metavar="BUILD_TYPE",
        type=str,
        choices=BUILD_TYPES,
        default=DEFAULT_BUILD_TYPE,
        help="Type of build (Debug or Release)"
    )
    parser.add_argument(
        '-j', '--jobs',
        type=int,
        default=DEFAULT_JOBS,
        help='Number of jobs for parallel compilation (default: maximum available)'
    )
    parser.add_argument(
        "--clean",
        type=str,
        metavar="CLEAN_TYPE",
        choices=CLEAN_TYPES,
        default=None,
        help="Clean build artifacts after compilation"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Disable progress bar and output analysis"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without actual compilation'
    )
    parser.add_argument(
        '--build-dir',
        type=str,
        default=f'{cwd}',
        help='Directory to perform the build in'
    )
    args = parser.parse_args()

    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Build type: {args.build_type}", 36)
    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Number of jobs: {args.jobs}", 36)
    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Verbose mode: {args.verbose}", 36)
    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Dry run: {args.dry_run}", 36)
    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Build directory: {args.build_dir}", 36)
    
    setup_check()
    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Project setup check complete.", 32)
    

    success = configure_project(args.build_type, args.build_dir, args.jobs, args.verbose, args.dry_run)

    build_end = time.time()
    total_compilation_time = build_end - build_start
    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Total compilation time: {total_compilation_time:.2f} seconds", 36)

    if success:
        print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Successfully built Ravi.", 32)
        os.chdir(cwd)

        # Determine the correct path to the executable in the build directory
        exe_name = "Ravi.exe" if sys.platform.startswith("win") else "Ravi"
        exe_path = os.path.join(args.build_dir, f"bin/{args.build_type}/" + exe_name)


    
        # Copy the executable to the destination directory
        if os.path.exists(exe_path):
            shutil.copy(exe_path, cwd) 
            print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Copied {exe_name} to {cwd}.", 32)
        else:
            print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] {exe_name} not found in {args.build_dir}!", 31)

        print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Build finished.", 32)
    else:
        print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Build failed!", 31)


    # Cleaning if requested
    if args.clean is not None:
        print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Cleaning build artifacts using clean type: {args.clean}", 34)
        Cleaner.Clean(args.clean, args.build_dir)
        print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Cleaning completed.", 32)

    
    end_time = time.time();
    total_time = end_time - build_start
    print_colored(f"[{datetime.now().strftime('%H:%M:%S')}] Total time taken: {total_time:.2f}s", 36)

if __name__ == "__main__":
    main()