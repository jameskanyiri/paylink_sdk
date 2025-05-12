#!/usr/bin/env python3
"""
Automated build and publish script for paylink-sdk
This script handles versioning, building, and publishing to PyPI.
"""

import os
import re
import subprocess
import argparse
from pathlib import Path

# Define version regex pattern
VERSION_PATTERN = r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]'

def get_current_version():
    """Extract the current version from __init__.py"""
    init_file = Path("src/paylink_sdk/__init__.py")
    if not init_file.exists():
        print(f"Error: {init_file} not found.")
        return None
    
    with open(init_file, "r") as f:
        content = f.read()
    
    match = re.search(VERSION_PATTERN, content)
    if match:
        return match.group(1)
    else:
        print(f"Warning: No version found in {init_file}")
        return None

def bump_version(current_version, bump_type):
    """Bump the version according to semantic versioning"""
    if not current_version:
        return None
    
    major, minor, patch = map(int, current_version.split('.'))
    
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"

def update_version_in_file(new_version):
    """Update the version in __init__.py"""
    init_file = Path("src/paylink_sdk/__init__.py")
    
    with open(init_file, "r") as f:
        content = f.read()
    
    updated_content = re.sub(
        VERSION_PATTERN,
        f'__version__ = "{new_version}"',
        content
    )
    
    with open(init_file, "w") as f:
        f.write(updated_content)
    
    print(f"Version updated to {new_version} in {init_file}")

def run_command(command, description=None):
    """Run a shell command and handle errors"""
    if description:
        print(f"\n{description}...")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        return False

def clean_build_artifacts():
    """Clean up build artifacts"""
    for directory in ["dist"]:
        run_command(f"rm -rf {directory}", f"Cleaning {directory}")
        
    # Also remove __pycache__ folders
    run_command("find . -type d -name '__pycache__' -exec rm -r {} +", "Removing __pycache__")
    run_command("find . -type f -name '*.pyc' -delete", "Removing .pyc files")

def main():
    parser = argparse.ArgumentParser(description="Build and publish paylink-sdk")
    parser.add_argument(
        "--bump", 
        choices=["major", "minor", "patch"], 
        default="patch",
        help="Version bump type (default: patch)"
    )
    
    # Add a publish target argument with choices
    parser.add_argument(
        "--publish",
        choices=["pypi", "testpypi", "none"],
        default="none",
        help="Where to publish the package (default: none)"
    )
    
    args = parser.parse_args()
    
    # Get current version
    current_version = get_current_version()
    if not current_version:
        print("Failed to determine current version. Exiting.")
        return 1
    
    print(f"Current version: {current_version}")
    
    # Bump version
    new_version = bump_version(current_version, args.bump)
    print(f"New version will be: {new_version}")
    
    # Update version in file
    update_version_in_file(new_version)
    
    # Clean previous builds
    clean_build_artifacts()
    
    # Build the package
    if not run_command("python -m hatch build", "Building package"):
        return 1
    
    # Run tests before publishing
    if not run_command("python -m pytest", "Running tests"):
        response = input("Tests failed. Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return 1
    
    # Publish if requested
    if args.publish != "none":
        repository_flag = "--repository testpypi" if args.publish == "testpypi" else ""
        publish_target = "TestPyPI" if args.publish == "testpypi" else "PyPI"
        
        if not run_command(f"python -m twine upload {repository_flag} dist/*", f"Publishing to {publish_target}"):
            return 1
        
        # Create git tag and push
        run_command(f"git add src/paylink_sdk/__init__.py", "Adding version change to git")
        run_command(f"git commit -m \"Bump version to {new_version}\"", "Committing version change")
        run_command(f"git tag v{new_version}", "Creating version tag")
        run_command("git push && git push --tags", "Pushing to remote repository")
        
    print(f"\nBuild completed successfully for paylink-sdk v{new_version}")
    if args.publish == "none":
        print("To publish to PyPI: python build_and_publish.py --publish pypi")
        print("To publish to TestPyPI: python build_and_publish.py --publish testpypi")
    
    return 0

if __name__ == "__main__":
    exit(main())