# capstone-project/semgrep_windows.py
import sys
import re

def main():
    # pre-commit passes the staged files as arguments
    files_to_scan = sys.argv[1:]
    if not files_to_scan:
        files_to_scan = ["app/agent.py"]
        
    # Split prefix to prevent matching itself
    pattern = re.compile(r'AIza' + r'Sy[A-Za-z0-9_\-]*')
    found_issue = False
    
    for filepath in files_to_scan:
        # Don't scan the helper script itself
        if "semgrep_windows.py" in filepath:
            continue
            
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            matches = pattern.findall(content)
            if matches:
                print(f"{filepath}")
                print("  Security Issue: Hardcoded Google API key prefix detected.")
                found_issue = True
        except Exception:
            pass
            
    if found_issue:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
