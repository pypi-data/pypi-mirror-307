from setuptools import setup, find_packages
import os
import stat

def post_install():
    """Post installation script to set permissions"""
    try:
        # Get the user's home directory
        home = os.path.expanduser("~")
        script_path = os.path.join(home, ".local", "bin", "discord-compress")
        
        if os.path.exists(script_path):
            # Set executable permissions (rwxr-xr-x)
            os.chmod(script_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    except Exception as e:
        print(f"Warning: Could not set permissions: {e}")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="discord-file-compressor",
    version="0.1.5",
    author="Abdude790",
    author_email="your.email@example.com",
    description="A tool to compress files for Discord's 10MB limit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abdude790/discord-file-compressor",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=9.0.0",
        "pyperclip>=1.8.2",
        "plyer>=2.1.0",
    ],
    entry_points={
        "console_scripts": [
            "discord-compress=discord_compressor.cli:main",
        ],
    },
    scripts=['scripts/post_install.py'],
) 