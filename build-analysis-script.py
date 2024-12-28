import os
import glob

def analyze_builds():
    # Dictionary to store problem results across all builds
    all_problems = {}

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

                    # Check if it's a pass or failure
                    is_pass = status == '.'
                    is_failure = status in 'CScemnpwrRT'

                    if is_pass or is_failure:
                        if prob_name not in all_problems:
                            all_problems[prob_name] = {'pass': False, 'fail': False}
                        
                        if is_pass:
                            all_problems[prob_name]['pass'] = True
                        elif is_failure:
                            all_problems[prob_name]['fail'] = True

    # Output problems that never pass
    print("Problems that never pass in any build:")
    for prob, results in all_problems.items():
        if results['fail'] and not results['pass']:
            print(prob)

if __name__ == "__main__":
    analyze_builds()
