#!/usr/bin/env python3
"""
SpaceGram Rename Automation Script for Telegram-iOS source code.
Usage:
    python rename_to_spacegram.py --repo-dir /path/to/Telegram-iOS
"""

import os
import re
import argparse
from pathlib import Path

REPLACEMENTS = [
    # Display names
    (r'"CFBundleDisplayName"\s*=\s*"Telegram"', '"CFBundleDisplayName" = "SpaceGram"'),
    (r'<key>CFBundleDisplayName</key>\s*<string>Telegram</string>', '<key>CFBundleDisplayName</key>\n\t<string>SpaceGram</string>'),
    (r'"AppName"\s*=\s*"Telegram"', '"AppName" = "SpaceGram"'),
    
    # App Names in Localizations
    (r'"ApplicationName"\s*=\s*"Telegram"', '"ApplicationName" = "SpaceGram"'),
]

TARGET_EXTENSIONS = {'.strings', '.plist', '.json', '.bzl', '.podspec', '.swift'}

def rename_in_file(filepath: Path):
    try:
        content = filepath.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError):
        return False

    modified = False
    new_content = content

    # 1. Regex replacements
    for pattern, repl in REPLACEMENTS:
        if re.search(pattern, new_content):
            new_content = re.sub(pattern, repl, new_content)
            modified = True

    # 2. Specific Info.plist CFBundleName
    if filepath.name in ['Info.plist', 'BuildVars.json', 'Config.json']:
        if '"Telegram"' in new_content:
            new_content = new_content.replace('"Telegram"', '"SpaceGram"')
            modified = True

    if modified:
        filepath.write_text(new_content, encoding='utf-8')
        print(f"[MODIFIED] {filepath}")
        return True
    return False

def scan_and_rename(root_dir: Path):
    count = 0
    print(f"[*] Scanning {root_dir} for Telegram branding...")
    
    for path in root_dir.rglob('*'):
        if path.is_file() and path.suffix in TARGET_EXTENSIONS:
            # Skip build caches / git
            if any(part in path.parts for part in ['.git', 'bazel-bin', 'bazel-out', 'build']):
                continue
            if rename_in_file(path):
                count += 1
                
    print(f"[+] Done. Modified {count} files.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rename Telegram to SpaceGram")
    parser.add_argument("--repo-dir", default=".", help="Path to Telegram-iOS repo")
    args = parser.parse_args()
    scan_and_rename(Path(args.repo_dir).resolve())
