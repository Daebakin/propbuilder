#!/usr/bin/env python3
import re
import os
import sys
from pathlib import Path

def extract_files(content):
    files = {}
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line and (line[0].isdigit() or '.php' in line or '.py' in line or '.js' in line):
            file_path = line
            if line[0].isdigit() and ' ' in line:
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    file_path = parts[1]
            
            i += 1
            if i < len(lines) and lines[i].strip() in ['php', 'python', 'javascript', 'js', 'vue', 'dart']:
                i += 1
            
            code_lines = []
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line and (next_line[0].isdigit() or '.php' in next_line or '.py' in next_line):
                    break
                if next_line != '```':
                    code_lines.append(lines[i])
                i += 1
            
            code = '\n'.join(code_lines).strip()
            code = re.sub(r'^```\w*\n?', '', code)
            code = re.sub(r'\n?```$', '', code)
            
            if file_path and code:
                files[file_path] = code
    
    return files

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_files.py <input_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        content = f.read()
    
    files = extract_files(content)
    
    for file_path, code in files.items():
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(code)
        print(f"✅ Created: {file_path}")
    
    print(f"\n📊 Total files created: {len(files)}")

if __name__ == "__main__":
    main()