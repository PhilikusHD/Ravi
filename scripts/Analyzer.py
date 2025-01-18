import re
from scripts.Utils import print_colored

def analyze_output(output):
    """
    Analyze the build output and extract warnings, errors, and linker errors.

    Parameters
    ----------
    output : str
        The build output.

    Returns
    -------
    warnings : list of str
        The warnings found in the build output.
    errors : list of str
        The errors found in the build output.
    linker_errors : list of str
        The linker errors found in the build output.
    """
    warnings = []
    errors = []
    linker_errors = []

    # Match warnings
    warning_regex = r"(.*):(\d+):(\d+):\s+warning:\s+(.*)"
    for line in output.splitlines():
        match = re.search(warning_regex, line)
        if match:
            warnings.append(f"{match.group(1)}:{match.group(2)}:{match.group(3)}: {match.group(4)}")

    # Match errors
    error_regex = r"(.*):(\d+):(\d+):\s+error:\s+(.*)"
    for line in output.splitlines():
        match = re.search(error_regex, line)
        if match:
            errors.append(f"{match.group(1)}:{match.group(2)}:{match.group(3)}: {match.group(4)}")

    # Match linker errors
    linker_error_regex = r"(ld: .*|/usr/bin/ld: .*)"
    for line in output.splitlines():
        match = re.search(linker_error_regex, line)
        if match:
            linker_errors.append(match.group(0))
    
    # Remove duplicates
    warnings = list(set(warnings))
    errors = list(set(errors))
    linker_errors = list(set(linker_errors))

    format_errors(errors, warnings, linker_errors)

    return errors, warnings, linker_errors


def format_errors(errors, warnings, linker_errors):
    """
    Formats the errors, warnings, and linker errors into a human-readable string.

    Parameters
    ----------
    errors : list of str
        The errors found in the build output.
    warnings : list of str
        The warnings found in the build output.
    linker_errors : list of str
        The linker errors found in the build output.

    Returns
    -------
	errMsg : str
		The formatted error message.
	warnMsg : str
		The formatted warning message.
	linkMsg : str
		The formatted linker error message.
    """

    errMsg = ""
    warnMsg = ""
    linkMsg = ""

    if warnings:
        warnMsg += "\nThe following warnings were found:\n"
        for i, warning in enumerate(warnings, start=1):
            warnMsg += f"{i}. {warning}\n"
        print_colored(warnMsg, 33)
    if errors:
        errMsg += "The following errors were found:\n"
        for i, error in enumerate(errors, start=1):
            errMsg += f"{i}. {error}\n"
        print_colored(errMsg, 91)

    if linker_errors:
        linkMsg += "\nThe following linker errors were found:\n"
        for i, linker_error in enumerate(linker_errors, start=1):
            linkMsg += f"{i}. {linker_error}\n"
        print_colored(linkMsg, 31)

    if errMsg == "" and warnMsg == "" and linkMsg == "":
        print_colored("\nNo errors or warnings were found.", 32)
    else:
        # Display number of warnings, errors and linker errors
        print_colored(f"Found {len(errors)} errors", 91)
        print_colored(f"Found {len(warnings)} warnings", 33)
        print_colored(f"Found {len(linker_errors)} linker errors.\n", 31)

    return errMsg, warnMsg, linkMsg