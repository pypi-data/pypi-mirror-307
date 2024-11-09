#!python
import os
import stat
import sys

def set_permissions():
    """Set proper permissions for the discord-compress command"""
    try:
        # Get the script path
        if sys.platform == "win32":
            script_path = os.path.join(sys.prefix, "Scripts", "discord-compress.exe")
        else:
            script_path = os.path.join(sys.prefix, "bin", "discord-compress")

        if os.path.exists(script_path):
            # Set executable permissions (rwxr-xr-x)
            os.chmod(script_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            print(f"Successfully set permissions for {script_path}")
    except Exception as e:
        print(f"Warning: Could not set permissions: {e}")

if __name__ == "__main__":
    set_permissions() 