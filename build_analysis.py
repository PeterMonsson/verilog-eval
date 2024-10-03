import os
import glob
from collections import defaultdict

def analyze_builds():
    # Dictionary to store problem results across all builds
    all_problems = defaultdict(lambda: {'pass': False, 'compile_errors': set(), 'runtime_errors': set()})

    # Mapping of error codes to their meanings
    error_meanings = {
        # Compile-time errors
        'C': 'General Compiler Error',
        'S': 'Syntax Error',
        'c': 'Unable to Bind Wire/Reg `clk`',
        'e': 'Explicit Cast Required',
        'm': 'Module Missing',
        'n': 'Sensitivity Problem',
        'p': 'Unable to Bind Wire/Reg',
        'w': 'Reg Declared as Wire',
        # Runtime errors
        'r': 'Reset Issue',
        'R': 'General Runtime Error',
        'T': 'Timeout'
    }

    # Sets of compile-time and runtime error codes
    compile_errors = {'C', 'S', 'c', 'e', 'm', 'n', 'p', 'w'}
    runtime_errors = {'r', 'R', 'T'}

    # Find all directories starting with 'build'
    build_dirs = glob.glob('build*')

    for build_dir in build_dirs:
        summary_file = os.path.join(build_dir, 'summary.txt')
        
        if not os.path.exists(summary_file):
            continue

        with open(summary_file, 'r') as f:
            for line in f:
                if line.startswith('Prob'):
                    parts = line.split()
                    prob_name = parts[0]
                    status = line.strip()[-1]

                    # Check if it's a pass or error
                    if status == '.':
                        all_problems[prob_name]['pass'] = True
                    elif status in compile_errors:
                        all_problems[prob_name]['compile_errors'].add(status)
                    elif status in runtime_errors:
                        all_problems[prob_name]['runtime_errors'].add(status)

    # Output problems that never pass and their error reasons
    print("Problems that never pass in any build and their error reasons:")
    for prob, results in all_problems.items():
        if not results['pass'] and (results['compile_errors'] or results['runtime_errors']):
            print(f"\n{prob}:")
            if results['compile_errors']:
                compile_descriptions = [f"{code} ({error_meanings[code]})" for code in results['compile_errors']]
                print("  Compile-time errors: " + ", ".join(compile_descriptions))
            if results['runtime_errors']:
                runtime_descriptions = [f"{code} ({error_meanings[code]})" for code in results['runtime_errors']]
                print("  Runtime errors: " + ", ".join(runtime_descriptions))

if __name__ == "__main__":
    analyze_builds()

