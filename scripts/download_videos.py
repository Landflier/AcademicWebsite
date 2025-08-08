#!/usr/bin/env python3
"""
YouTube Video Downloader for Academic Website
Downloads YouTube videos for local backup and long-term preservation.

Requirements:
    pip install yt-dlp

Usage:
    python scripts/download_videos.py --video-id <YOUTUBE_ID> [--output-dir <DIR>]
    python scripts/download_videos.py --batch-file docs/video_list_example.txt
"""

import argparse
import os
import sys
import json
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is required. Install with: pip install yt-dlp")
    sys.exit(1)


class VideoDownloader:
    def __init__(self, output_dir="static/videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # yt-dlp options for high quality, web-friendly format
        self.ydl_opts = {
            'format': 'best[ext=mp4][height<=720]/best[ext=mp4]/best',
            'outtmpl': str(self.output_dir / '%(id)s.%(ext)s'),
            'writeinfojson': True,  # Save metadata
            'writethumbnail': True,  # Save thumbnail
            'writesubtitles': True,  # Save subtitles if available
            'writeautomaticsub': False,  # Skip auto-generated subs
        }

    def download_video(self, video_id):
        """Download a single YouTube video"""
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        print(f"Downloading video: {video_id}")
        print(f"URL: {url}")
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Get info first
                info = ydl.extract_info(url, download=False)
                print(f"Title: {info.get('title', 'Unknown')}")
                print(f"Duration: {info.get('duration', 'Unknown')} seconds")
                print(f"Upload date: {info.get('upload_date', 'Unknown')}")
                
                # Download
                ydl.download([url])
                
                # Create Hugo shortcode example
                self._create_shortcode_example(video_id, info)
                
                print(f"✓ Successfully downloaded: {video_id}")
                return True
                
        except Exception as e:
            print(f"✗ Error downloading {video_id}: {e}")
            return False

    def _create_shortcode_example(self, video_id, info):
        """Create example Hugo shortcode usage"""
        title = info.get('title', 'Video Title')
        description = info.get('description', '')[:200] + "..." if info.get('description') else ""
        
        shortcode = f'''
<!-- Example Hugo shortcode for video {video_id} -->
{{{{< video 
    youtube="{video_id}"
    local="/videos/{video_id}.mp4"
    title="{title}"
    description="{description}"
    width="100%"
    height="400px" >}}}}
'''
        
        example_file = self.output_dir / f"{video_id}_shortcode_example.md"
        with open(example_file, 'w', encoding='utf-8') as f:
            f.write(shortcode)
        
        print(f"Example shortcode saved to: {example_file}")

    def download_batch(self, batch_file):
        """Download multiple videos from a file containing video IDs"""
        if not os.path.exists(batch_file):
            print(f"Error: Batch file {batch_file} not found")
            return False
        
        success_count = 0
        total_count = 0
        
        with open(batch_file, 'r') as f:
            for line in f:
                video_id = line.strip()
                if video_id and not video_id.startswith('#'):
                    total_count += 1
                    if self.download_video(video_id):
                        success_count += 1
                    print("-" * 50)
        
        print(f"\nDownload complete: {success_count}/{total_count} successful")
        return success_count == total_count

    def list_downloaded(self):
        """List all downloaded videos"""
        videos = list(self.output_dir.glob("*.mp4"))
        if not videos:
            print("No downloaded videos found")
            return
        
        print(f"Downloaded videos in {self.output_dir}:")
        for video in videos:
            # Try to load metadata
            info_file = video.with_suffix('.info.json')
            if info_file.exists():
                with open(info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    title = info.get('title', 'Unknown')
                    duration = info.get('duration', 'Unknown')
                    print(f"  {video.name} - {title} ({duration}s)")
            else:
                print(f"  {video.name}")


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos for academic website")
    parser.add_argument('--video-id', help='YouTube video ID to download')
    parser.add_argument('--batch-file', help='File containing list of video IDs')
    parser.add_argument('--output-dir', default='static/videos', 
                       help='Output directory for videos (default: static/videos)')
    parser.add_argument('--list', action='store_true', 
                       help='List already downloaded videos')
    
    args = parser.parse_args()
    
    downloader = VideoDownloader(args.output_dir)
    
    if args.list:
        downloader.list_downloaded()
    elif args.video_id:
        downloader.download_video(args.video_id)
    elif args.batch_file:
        downloader.download_batch(args.batch_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()