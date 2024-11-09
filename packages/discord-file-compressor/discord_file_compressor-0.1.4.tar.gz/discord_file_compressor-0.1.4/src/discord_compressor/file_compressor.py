import os
import subprocess
from PIL import Image
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10MB in bytes

class FileCompressor:
    def __init__(self, input_path: str, target_size: int = MAX_SIZE_BYTES):
        self.input_path = Path(input_path)
        self.target_size = target_size
        self.output_path = self.input_path.parent / f"compressed_{self.input_path.name}"

    def compress(self) -> Path:
        """Compress file based on its type"""
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input file {self.input_path} does not exist")

        file_size = os.path.getsize(self.input_path)
        if file_size <= self.target_size:
            logger.info("File is already smaller than target size")
            return self.input_path

        file_type = self.input_path.suffix.lower()
        
        # Extended video formats
        VIDEO_FORMATS = [
            '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.m4v', 
            '.3gp', '.mpeg', '.mpg', '.m2v', '.ts', '.mts', '.m2ts'
        ]
        
        # Extended image formats
        IMAGE_FORMATS = [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp',
            '.heic', '.heif', '.raw', '.cr2', '.nef', '.arw'
        ]
        
        if file_type in VIDEO_FORMATS:
            return self._compress_video()
        elif file_type in IMAGE_FORMATS:
            return self._compress_image()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def _compress_video(self) -> Path:
        """Compress video using ffmpeg with adaptive bitrate"""
        try:
            # Get video duration and original bitrate
            probe = subprocess.run([
                'ffprobe', '-v', 'error', '-show_entries', 
                'format=duration,bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', 
                str(self.input_path)
            ], capture_output=True, text=True)
            
            probe_output = probe.stdout.strip().split('\n')
            duration = float(probe_output[0])
            
            # Calculate target bitrate (bits/second)
            target_bitrate = int((self.target_size * 8) / duration * 0.95)  # 95% of target size
            
            # Enhanced compression settings
            subprocess.run([
                'ffmpeg', '-i', str(self.input_path),
                '-c:v', 'libx264', '-crf', '28',  # Slightly more compression
                '-maxrate', f'{target_bitrate}',
                '-bufsize', f'{target_bitrate * 2}',
                '-preset', 'slower',  # Better compression
                '-movflags', '+faststart',  # Enables streaming
                '-c:a', 'aac', '-b:a', '96k',  # Reduced audio bitrate
                '-y',  # Overwrite output file if it exists
                str(self.output_path)
            ], check=True)
            
            return self.output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Error compressing video: {e}")
            raise

    def _compress_image(self) -> Path:
        """Compress image using PIL with adaptive quality"""
        try:
            img = Image.open(self.input_path)
            
            # Convert HEIC/HEIF to JPEG first
            if self.input_path.suffix.lower() in ['.heic', '.heif']:
                self.output_path = self.output_path.with_suffix('.jpg')
            
            # Convert to RGB if necessary
            if img.mode in ['RGBA', 'P']:
                img = img.convert('RGB')
            
            # Calculate max dimensions while maintaining aspect ratio
            max_dimension = 4000  # Maximum dimension for any side
            ratio = min(max_dimension / max(img.size[0], img.size[1]), 1.0)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            
            if ratio < 1.0:
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Progressive quality reduction
            quality = 95
            while quality > 5:
                img.save(self.output_path, 
                        quality=quality, 
                        optimize=True,
                        progressive=True)  # Progressive JPEG
                if os.path.getsize(self.output_path) <= self.target_size:
                    break
                quality -= 5
            
            return self.output_path
        except Exception as e:
            logger.error(f"Error compressing image: {e}")
            raise