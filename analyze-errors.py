import os
import re
from collections import Counter

ERROR_TYPES = {
    'C': 'General Compiler Error',
    'S': 'Syntax Error',
    'c': 'Unable to Bind Wire/Reg `clk`',
    'e': 'Explicit Cast Required',
    'm': 'Module Missing',
    'n': 'Sensitivity Problem',
    'p': 'Unable to Bind Wire/Reg',
    'w': 'Reg Declared as Wire',
    'r': 'Reset Issue',
    'R': 'General Runtime Error',
    'T': 'Timeout'
}

def read_summary_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def extract_error_directories_and_types(summary_lines):
    error_dirs = []
    for line in summary_lines:
        if line.startswith('Prob') and not line.strip().endswith('.'):
            parts = line.split()
            if len(parts) >= 1:
                directory = parts[0]
                error_type = line.strip()[-1]
                error_dirs.append((directory, error_type))
    return error_dirs

def find_first_error(log_file_path, error_type):
    with open(log_file_path, 'r') as file:
        if error_type in ('r', 'R'):
            pattern = r"Hint: Output '[^']*' has (\d+) mismatches\. First mismatch occurred at time (\d+)\."
            for line in file:
                match = re.search(pattern, line)
                if match:
                    mismatches, time = match.groups()
                    return line.strip()
            return "No error found in the log file."
        else:
            for line in file:
                if 'error' in line.lower():
                    return line.strip()
                if 'warning' in line.lower():
                    return line.strip()
    return "No error found in the log file."

def main():
    summary_file = 'summary.txt'
    
    if not os.path.exists(summary_file):
        print(f"Error: {summary_file} not found.")
        return

    summary_lines = read_summary_file(summary_file)
    error_directories_and_types = extract_error_directories_and_types(summary_lines)
    error_types = Counter()

    for directory, error_type in error_directories_and_types:
        log_file = f"{directory}/{directory}_sample01-sv-iv-test.log"
        if os.path.exists(log_file):
            error = find_first_error(log_file, error_type)
            error_types[error_type] += 1
            print(f"{directory} ({ERROR_TYPES.get(error_type, 'Unknown Error Type')}): {error}")
        else:
            print(f"{directory}: Log file not found.")

    print("\nError Type Summary:")
    for error_type, count in error_types.items():
        print(f"{error_type} - {ERROR_TYPES.get(error_type, 'Unknown Error Type')}: {count}")

if __name__ == "__main__":
    main()
