#!/usr/bin/env python3
"""
Script to recursively list all files in the same directory and subdirectories,
saving to a timestamped text file with directory structure.
"""

import os
from datetime import datetime


def get_all_files(root_dir):
    """
    Recursively get all files organized by directory.
    Returns a dict: {relative_dir_path: [list of filenames]}
    """
    files_by_dir = {}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Get relative path from root
        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path == ".":
            rel_path = "(root)"
        
        # Sort filenames and dirnames for consistent output
        dirnames.sort()
        filenames.sort()
        
        if filenames:  # Only include directories that have files
            files_by_dir[rel_path] = filenames
    
    return files_by_dir


def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get all files recursively
    files_by_dir = get_all_files(script_dir)
    
    # Count total files
    total_files = sum(len(files) for files in files_by_dir.values())
    total_dirs = len(files_by_dir)
    
    # Generate timestamp in YYMMDD_HHMMSS format
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    
    # Create output filename
    output_filename = f"{timestamp}_File_List.txt"
    output_path = os.path.join(script_dir, output_filename)
    
    # Write file names to the output file
    with open(output_path, 'w') as f:
        f.write(f"File List Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Directory Root: {script_dir}\n")
        f.write(f"Total Files: {total_files}\n")
        f.write(f"Total Directories with Files: {total_dirs}\n")
        f.write("=" * 60 + "\n\n")
        
        # Sort directories for consistent output
        sorted_dirs = sorted(files_by_dir.keys(), key=lambda x: (x != "(root)", x))
        
        for dir_path in sorted_dirs:
            files = files_by_dir[dir_path]
            f.write(f"[{dir_path}]\n")
            f.write("-" * 40 + "\n")
            for filename in files:
                f.write(f"  {filename}\n")
            f.write("\n")
    
    print(f"Created: {output_filename}")
    print(f"Listed {total_files} files across {total_dirs} directories")


if __name__ == "__main__":
    main()
