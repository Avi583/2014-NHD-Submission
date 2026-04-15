#!/usr/bin/env python3
"""
Scan code files for imports, exports, and URLs.
Recursively processes all coding scripts in the current folder and subfolders.
Outputs results to a timestamped text file.
"""

import os
import re
from datetime import datetime
from pathlib import Path


# File extensions to scan (coding scripts only)
CODE_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
    '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.php', '.rb', '.java', '.c', '.cpp', '.h', '.hpp',
    '.cs', '.go', '.rs', '.swift', '.kt', '.scala',
    '.vue', '.svelte', '.astro', '.json', '.xml', '.yaml', '.yml',
    '.sh', '.bash', '.zsh', '.ps1', '.bat', '.cmd',
    '.sql', '.r', '.R', '.lua', '.pl', '.pm'
}

# Extensions to skip (documents, images, etc.)
SKIP_EXTENSIONS = {
    '.doc', '.docx', '.pdf', '.txt', '.md', '.rtf', '.odt',
    '.xls', '.xlsx', '.csv', '.ppt', '.pptx',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp',
    '.mp3', '.mp4', '.wav', '.avi', '.mov', '.mkv',
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.exe', '.dll', '.so', '.dylib', '.bin',
    '.pyc', '.pyo', '.class', '.o', '.obj'
}


def extract_python_imports(content: str) -> list[str]:
    """Extract Python import statements."""
    imports = []
    
    # import module / import module as alias
    pattern1 = r'^import\s+([\w\.]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w\.]+(?:\s+as\s+\w+)?)*)'
    for match in re.finditer(pattern1, content, re.MULTILINE):
        imports.append(f"import {match.group(1)}")
    
    # from module import ...
    pattern2 = r'^from\s+([\w\.]+)\s+import\s+(.+?)(?:\s*#.*)?$'
    for match in re.finditer(pattern2, content, re.MULTILINE):
        imports.append(f"from {match.group(1)} import {match.group(2).strip()}")
    
    return imports


def extract_js_imports_exports(content: str) -> dict[str, list[str]]:
    """Extract JavaScript/TypeScript imports and exports."""
    result = {'imports': [], 'exports': []}
    
    # ES6 imports: import ... from '...'
    import_pattern = r'''import\s+(?:(?:[\w*{}\s,]+)\s+from\s+)?['"]([^'"]+)['"]'''
    for match in re.finditer(import_pattern, content):
        result['imports'].append(f"import from '{match.group(1)}'")
    
    # require() statements
    require_pattern = r'''require\s*\(\s*['"]([^'"]+)['"]\s*\)'''
    for match in re.finditer(require_pattern, content):
        result['imports'].append(f"require('{match.group(1)}')")
    
    # Dynamic imports
    dynamic_pattern = r'''import\s*\(\s*['"]([^'"]+)['"]\s*\)'''
    for match in re.finditer(dynamic_pattern, content):
        result['imports'].append(f"dynamic import('{match.group(1)}')")
    
    # Exports
    export_patterns = [
        r'^export\s+(?:default\s+)?(?:class|function|const|let|var|async)\s+(\w+)',
        r'^export\s+\{([^}]+)\}',
        r'^export\s+default\s+(\w+)',
        r'^module\.exports\s*=',
        r'^exports\.(\w+)\s*='
    ]
    for pattern in export_patterns:
        for match in re.finditer(pattern, content, re.MULTILINE):
            if match.groups():
                result['exports'].append(f"export {match.group(1)}")
            else:
                result['exports'].append("module.exports")
    
    return result


def extract_html_references(content: str) -> dict[str, list[str]]:
    """Extract HTML script/link/img references."""
    result = {'scripts': [], 'stylesheets': [], 'images': []}
    
    # Script src
    script_pattern = r'<script[^>]*\ssrc=["\']([^"\']+)["\']'
    for match in re.finditer(script_pattern, content, re.IGNORECASE):
        result['scripts'].append(match.group(1))
    
    # Link href (stylesheets)
    link_pattern = r'<link[^>]*\shref=["\']([^"\']+)["\'][^>]*(?:rel=["\']stylesheet["\']|\.css)'
    for match in re.finditer(link_pattern, content, re.IGNORECASE):
        result['stylesheets'].append(match.group(1))
    
    # Also check for rel="stylesheet" pattern
    link_pattern2 = r'<link[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']'
    for match in re.finditer(link_pattern2, content, re.IGNORECASE):
        if match.group(1) not in result['stylesheets']:
            result['stylesheets'].append(match.group(1))
    
    # Image src
    img_pattern = r'<img[^>]*\ssrc=["\']([^"\']+)["\']'
    for match in re.finditer(img_pattern, content, re.IGNORECASE):
        result['images'].append(match.group(1))
    
    return result


def extract_css_imports(content: str) -> list[str]:
    """Extract CSS @import statements."""
    imports = []
    
    # @import url(...) or @import "..."
    pattern = r'@import\s+(?:url\s*\(\s*)?["\']?([^"\';\)\s]+)["\']?\s*\)?'
    for match in re.finditer(pattern, content, re.IGNORECASE):
        imports.append(f"@import {match.group(1)}")
    
    return imports


def extract_urls(content: str) -> list[str]:
    """Extract URLs from content."""
    urls = []
    
    # HTTP/HTTPS URLs
    url_pattern = r'https?://[^\s<>"\'`\)\]\}]+'
    for match in re.finditer(url_pattern, content):
        url = match.group(0).rstrip('.,;:')
        if url not in urls:
            urls.append(url)
    
    return urls


def extract_php_includes(content: str) -> list[str]:
    """Extract PHP include/require statements."""
    includes = []
    
    pattern = r'(?:include|require)(?:_once)?\s*\(?["\']([^"\']+)["\']\)?'
    for match in re.finditer(pattern, content):
        includes.append(f"include/require '{match.group(1)}'")
    
    return includes


def extract_java_imports(content: str) -> list[str]:
    """Extract Java import statements."""
    imports = []
    
    pattern = r'^import\s+([\w\.]+\*?)\s*;'
    for match in re.finditer(pattern, content, re.MULTILINE):
        imports.append(f"import {match.group(1)}")
    
    return imports


def extract_go_imports(content: str) -> list[str]:
    """Extract Go import statements."""
    imports = []
    
    # Single import
    single_pattern = r'^import\s+"([^"]+)"'
    for match in re.finditer(single_pattern, content, re.MULTILINE):
        imports.append(f'import "{match.group(1)}"')
    
    # Import block
    block_pattern = r'import\s*\((.*?)\)'
    for match in re.finditer(block_pattern, content, re.DOTALL):
        block = match.group(1)
        for line in block.split('\n'):
            line = line.strip()
            pkg_match = re.search(r'"([^"]+)"', line)
            if pkg_match:
                imports.append(f'import "{pkg_match.group(1)}"')
    
    return imports


def extract_ruby_requires(content: str) -> list[str]:
    """Extract Ruby require statements."""
    requires = []
    
    pattern = r'^(?:require|require_relative|load)\s+["\']([^"\']+)["\']'
    for match in re.finditer(pattern, content, re.MULTILINE):
        requires.append(f"require '{match.group(1)}'")
    
    return requires


def analyze_file(filepath: Path) -> dict:
    """Analyze a single file for imports, exports, and URLs."""
    result = {
        'imports': [],
        'exports': [],
        'urls': [],
        'references': {}
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        result['error'] = str(e)
        return result
    
    ext = filepath.suffix.lower()
    
    # Python
    if ext == '.py':
        result['imports'] = extract_python_imports(content)
    
    # JavaScript/TypeScript
    elif ext in {'.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.vue', '.svelte'}:
        js_result = extract_js_imports_exports(content)
        result['imports'] = js_result['imports']
        result['exports'] = js_result['exports']
    
    # HTML
    elif ext in {'.html', '.htm'}:
        html_refs = extract_html_references(content)
        result['references'] = html_refs
        # Also check for embedded JS imports
        js_result = extract_js_imports_exports(content)
        result['imports'].extend(js_result['imports'])
    
    # CSS
    elif ext in {'.css', '.scss', '.sass', '.less'}:
        result['imports'] = extract_css_imports(content)
    
    # PHP
    elif ext == '.php':
        result['imports'] = extract_php_includes(content)
        # PHP files often have HTML/JS too
        html_refs = extract_html_references(content)
        result['references'] = html_refs
    
    # Java
    elif ext == '.java':
        result['imports'] = extract_java_imports(content)
    
    # Go
    elif ext == '.go':
        result['imports'] = extract_go_imports(content)
    
    # Ruby
    elif ext == '.rb':
        result['imports'] = extract_ruby_requires(content)
    
    # C/C++ includes
    elif ext in {'.c', '.cpp', '.h', '.hpp', '.cc', '.cxx'}:
        pattern = r'^#include\s*[<"]([^>"]+)[>"]'
        for match in re.finditer(pattern, content, re.MULTILINE):
            result['imports'].append(f"#include {match.group(1)}")
    
    # Extract URLs from all file types
    result['urls'] = extract_urls(content)
    
    return result


def format_file_results(filepath: Path, results: dict, root_dir: Path) -> str:
    """Format the results for a single file."""
    relative_path = filepath.relative_to(root_dir)
    lines = [f"\n{'='*60}", f"FILE: {relative_path}", '='*60]
    
    if 'error' in results:
        lines.append(f"  ERROR: {results['error']}")
        return '\n'.join(lines)
    
    has_content = False
    
    if results['imports']:
        has_content = True
        lines.append("\n  IMPORTS:")
        for imp in results['imports']:
            lines.append(f"    - {imp}")
    
    if results['exports']:
        has_content = True
        lines.append("\n  EXPORTS:")
        for exp in results['exports']:
            lines.append(f"    - {exp}")
    
    if results['references']:
        for ref_type, refs in results['references'].items():
            if refs:
                has_content = True
                lines.append(f"\n  {ref_type.upper()}:")
                for ref in refs:
                    lines.append(f"    - {ref}")
    
    if results['urls']:
        has_content = True
        lines.append("\n  URLs:")
        for url in results['urls']:
            lines.append(f"    - {url}")
    
    if not has_content:
        lines.append("  (No imports, exports, or URLs found)")
    
    return '\n'.join(lines)


def scan_directory(directory: Path, root_dir: Path = None) -> list[tuple[Path, dict]]:
    """Recursively scan a directory for code files."""
    if root_dir is None:
        root_dir = directory
    
    results = []
    
    try:
        items = sorted(directory.iterdir())
    except PermissionError:
        return results
    
    for item in items:
        # Skip hidden files/folders
        if item.name.startswith('.'):
            continue
        
        # Skip common non-essential folders
        if item.is_dir() and item.name in {'node_modules', '__pycache__', 'venv', 'env', 
                                            '.git', '.svn', 'dist', 'build', '.idea', '.vscode'}:
            continue
        
        if item.is_file():
            ext = item.suffix.lower()
            if ext in CODE_EXTENSIONS and ext not in SKIP_EXTENSIONS:
                file_results = analyze_file(item)
                results.append((item, file_results))
                print(f"  ✓ Scanned: {item.relative_to(root_dir)}")
        
        elif item.is_dir():
            results.extend(scan_directory(item, root_dir))
    
    return results


def generate_directory_tree(directory: Path, prefix: str = "", root_dir: Path = None) -> str:
    """Generate a directory tree string."""
    if root_dir is None:
        root_dir = directory
    
    lines = []
    
    try:
        items = sorted(directory.iterdir())
    except PermissionError:
        return ""
    
    # Filter items
    dirs = []
    files = []
    for item in items:
        if item.name.startswith('.'):
            continue
        if item.is_dir():
            if item.name not in {'node_modules', '__pycache__', 'venv', 'env', 
                                 '.git', '.svn', 'dist', 'build', '.idea', '.vscode'}:
                dirs.append(item)
        elif item.is_file():
            ext = item.suffix.lower()
            if ext in CODE_EXTENSIONS:
                files.append(item)
    
    all_items = dirs + files
    
    for i, item in enumerate(all_items):
        is_last = (i == len(all_items) - 1)
        connector = "└── " if is_last else "├── "
        
        if item.is_dir():
            lines.append(f"{prefix}{connector}{item.name}/")
            extension = "    " if is_last else "│   "
            subtree = generate_directory_tree(item, prefix + extension, root_dir)
            if subtree:
                lines.append(subtree)
        else:
            lines.append(f"{prefix}{connector}{item.name}")
    
    return '\n'.join(lines)


def main():
    """Main function to run the scanner."""
    # Get the directory where the script is located (NOT cwd)
    script_dir = Path(__file__).parent.resolve()
    
    print(f"\n{'='*60}")
    print(f"IMPORT/EXPORT SCANNER")
    print(f"{'='*60}")
    print(f"Will scan: {script_dir}")
    print(f"{'='*60}\n")
    
    # Safety confirmation
    confirm = input("Proceed with scan? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Scan cancelled.")
        return
    
    print("\nLooking for code files...")
    
    # Scan all files
    all_results = scan_directory(script_dir)
    
    if not all_results:
        print("No code files found in this directory.")
        return
    
    print(f"Found {len(all_results)} code file(s)")
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    output_filename = f"{timestamp}_Imports_Exports.txt"
    output_path = script_dir / output_filename
    
    # Build output content
    output_lines = [
        "IMPORTS & EXPORTS SCAN REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Root Directory: {script_dir}",
        f"Files Scanned: {len(all_results)}",
        "\n" + "="*60,
        "DIRECTORY STRUCTURE",
        "="*60,
        f"{script_dir.name}/",
        generate_directory_tree(script_dir),
    ]
    
    # Group results by directory
    current_dir = None
    for filepath, results in all_results:
        parent = filepath.parent
        if parent != current_dir:
            current_dir = parent
            rel_parent = parent.relative_to(script_dir) if parent != script_dir else Path(".")
            output_lines.append(f"\n\n{'#'*60}")
            output_lines.append(f"# DIRECTORY: {rel_parent}")
            output_lines.append('#'*60)
        
        output_lines.append(format_file_results(filepath, results, script_dir))
    
    # Write output file
    output_content = '\n'.join(output_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"\nReport saved to: {output_filename}")
    print(f"Full path: {output_path}")


if __name__ == "__main__":
    main()
