#!/usr/bin/env python3
"""
Script to list all files in the same directory and save to a timestamped text file.
"""

import os
from datetime import datetime


def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get all file names in the directory
    all_items = os.listdir(script_dir)
    file_names = [item for item in all_items if os.path.isfile(os.path.join(script_dir, item))]
    
    # Sort alphabetically for consistency
    file_names.sort()
    
    # Generate timestamp in YYMMDD_HHMMSS format
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    
    # Create output filename
    output_filename = f"{timestamp}_File_List.txt"
    output_path = os.path.join(script_dir, output_filename)
    
    # Write file names to the output file
    with open(output_path, 'w') as f:
        f.write(f"File List Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Directory: {script_dir}\n")
        f.write(f"Total Files: {len(file_names)}\n")
        f.write("-" * 50 + "\n\n")
        
        for filename in file_names:
            f.write(f"{filename}\n")
    
    print(f"Created: {output_filename}")
    print(f"Listed {len(file_names)} files")


if __name__ == "__main__":
    main()
