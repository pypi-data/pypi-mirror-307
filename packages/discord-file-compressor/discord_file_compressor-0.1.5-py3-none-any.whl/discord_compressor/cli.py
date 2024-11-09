import os
import sys
import shutil
import pyperclip
from plyer import notification
from .file_compressor import FileCompressor

def check_ffmpeg():
    """Check if ffmpeg is installed"""
    if not shutil.which('ffmpeg'):
        print("\nError: ffmpeg is not installed!")
        print("\nTo install ffmpeg:")
        print("- On macOS: brew install ffmpeg")
        print("- On Windows: Download from https://ffmpeg.org/download.html")
        print("- On Ubuntu/Debian: sudo apt-get install ffmpeg")
        sys.exit(1)

def verify_file(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    print(f"\nFiles in directory {directory}:")
    for file in os.listdir(directory):
        print(f"- {file}")
    
    file_name = os.path.basename(file_path)
    print(f"\nLooking for exact file: {file_name}")

def notify_success(file_path: str) -> None:
    """Show notification and copy path to clipboard"""
    try:
        # Copy to clipboard
        pyperclip.copy(str(file_path))
        
        # Show notification
        notification.notify(
            title='File Compressed',
            message='Compressed file path copied to clipboard!',
            app_icon=None,
            timeout=10,
        )
        print("\nFile path copied to clipboard!")
    except Exception as e:
        print(f"\nNotification error: {e}")
        print("But compression was successful!")

def compress_file(file_path: str) -> None:
    try:
        abs_path = os.path.expanduser(file_path)
        print(f"Looking for file at: {abs_path}")
        
        if not os.path.exists(abs_path):
            print(f"\nError: File not found at {abs_path}")
            print("Make sure the file exists and the path is correct.")
            return
            
        original_size = os.path.getsize(abs_path) / (1024 * 1024)
        print(f"\nOriginal file size: {original_size:.2f} MB")
        
        if original_size <= 10:
            print("\nFile is already under 10MB! No compression needed.")
            return
        
        compressor = FileCompressor(abs_path)
        compressed_file = compressor.compress()
        
        compressed_size = os.path.getsize(compressed_file) / (1024 * 1024)
        print(f"\nCompressed file size: {compressed_size:.2f} MB")
        print(f"Compressed file saved to: {compressed_file}")
        
        # Copy to clipboard and notify
        notify_success(compressed_file)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nIf this is a video file, make sure ffmpeg is installed.")
        print("If the problem persists, please report the issue on GitHub.")
        sys.exit(1)

def main():
    print("\nDiscord File Compressor @Abdude790")
    print("-------------------")
    print("This tool will compress your file to under 10MB for Discord")
    print("\nSupported formats:")
    print("- Videos: MP4, MOV, AVI, MKV, WMV, FLV, WebM, and more")
    print("- Images: JPG, PNG, GIF, BMP, TIFF, WebP, HEIC, and more")
    print("\nEnter the path to your file. You can:")
    print("1. Drag and drop the file into the terminal")
    print("2. Copy and paste the full path")
    print("3. Use ~ for your home directory (e.g., ~/Desktop/video.mov)")
    
    # Check for ffmpeg
    check_ffmpeg()
    
    video_path = input("\nEnter file path: ").strip()
    video_path = video_path.strip("'\"")
    
    print(f"\nStarting compression for: {video_path}")
    compress_file(video_path)

if __name__ == "__main__":
    main() 