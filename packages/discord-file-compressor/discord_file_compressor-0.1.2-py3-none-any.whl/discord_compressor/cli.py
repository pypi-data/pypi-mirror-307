import os
import sys
from .file_compressor import FileCompressor

def verify_file(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    print(f"\nFiles in directory {directory}:")
    for file in os.listdir(directory):
        print(f"- {file}")
    
    file_name = os.path.basename(file_path)
    print(f"\nLooking for exact file: {file_name}")

def compress_file(file_path: str) -> None:
    verify_file(file_path)
    try:
        abs_path = os.path.expanduser(file_path)
        print(f"Looking for file at: {abs_path}")
        
        if not os.path.exists(abs_path):
            print(f"Error: File not found at {abs_path}")
            return
            
        original_size = os.path.getsize(abs_path) / (1024 * 1024)
        print(f"Original file size: {original_size:.2f} MB")
        
        compressor = FileCompressor(abs_path)
        compressed_file = compressor.compress()
        
        compressed_size = os.path.getsize(compressed_file) / (1024 * 1024)
        print(f"Compressed file size: {compressed_size:.2f} MB")
        print(f"Compressed file saved to: {compressed_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    print("Discord File Compressor @Abdude790")
    print("-------------------")
    print("Enter the path to your file. You can:")
    print("1. Drag and drop the file into the terminal")
    print("2. Copy and paste the full path")
    print("3. Use ~ for your home directory (e.g., ~/Desktop/video.mov)")
    
    video_path = input("\nEnter file path: ").strip()
    video_path = video_path.strip("'\"")
    
    print(f"\nStarting compression for: {video_path}")
    compress_file(video_path)

if __name__ == "__main__":
    main() 