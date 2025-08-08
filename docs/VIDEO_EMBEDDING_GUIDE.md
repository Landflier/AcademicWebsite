# Video Embedding Guide for Long-term Preservation

This guide explains how to embed YouTube videos in your Hugo academic website while ensuring they remain available long-term.

## Quick Start

### 1. Basic YouTube Embed (Least Reliable)
```hugo
{{< video youtube="dQw4w9WgXcQ" title="Example Video" >}}
```

### 2. YouTube with Local Backup (Recommended)
```hugo
{{< video 
    youtube="dQw4w9WgXcQ"
    local="/videos/dQw4w9WgXcQ.mp4"
    title="Example Video"
    description="A demonstration video about Gilbert cell design" >}}
```

### 3. YouTube with Multiple Fallbacks (Most Reliable)
```hugo
{{< video 
    youtube="dQw4w9WgXcQ"
    local="/videos/dQw4w9WgXcQ.mp4"
    archive="https://archive.org/details/your-video-backup"
    title="Example Video"
    description="A demonstration video about Gilbert cell design"
    width="100%"
    height="450px" >}}
```

## Video Preservation Workflow

### Step 1: Download Videos for Local Backup

Install the required tool:
```bash
pip install yt-dlp
```

Download a single video:
```bash
python scripts/download_videos.py --video-id dQw4w9WgXcQ
```

Download multiple videos (create a `video_list.txt` file with one video ID per line):
```bash
echo "dQw4w9WgXcQ" > video_list.txt
echo "kJQP7kiw5Fk" >> video_list.txt
python scripts/download_videos.py --batch-file video_list.txt
```

### Step 2: Upload to Internet Archive (Optional but Recommended)

1. Create an account at [archive.org](https://archive.org)
2. Upload your video with metadata
3. Note the archive.org URL for use in the shortcode

### Step 3: Use the Video Shortcode

The shortcode automatically:
- Shows YouTube embed by default (for performance)
- Falls back to local video if YouTube is unavailable
- Provides links to alternative sources
- Handles mobile responsiveness

## Shortcode Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `youtube` | No* | YouTube video ID | - |
| `local` | No* | Path to local video file | - |
| `archive` | No | Internet Archive URL | - |
| `title` | No | Video title for accessibility | "Video" |
| `description` | No | Video description | - |
| `width` | No | Video width | "100%" |
| `height` | No | Video height | "400px" |
| `fallback_message` | No | Custom error message | Default message |

*At least one of `youtube`, `local`, or `archive` must be provided.

## Directory Structure

```
static/
├── videos/                    # Local video backups
│   ├── dQw4w9WgXcQ.mp4       # Video file
│   ├── dQw4w9WgXcQ.info.json # Metadata
│   ├── dQw4w9WgXcQ.webp      # Thumbnail
│   └── ...
└── ...

scripts/
└── download_videos.py         # Download utility

layouts/shortcodes/
└── video.html                 # Video shortcode
```

## Best Practices

### 1. Multiple Preservation Strategies
- **Primary**: YouTube embed (fast loading, no bandwidth cost)
- **Secondary**: Local backup (your control, always available)
- **Tertiary**: Internet Archive (institutional preservation)

### 2. File Organization
- Store videos in `static/videos/` directory
- Use YouTube video ID as filename for consistency
- Keep metadata files for future reference

### 3. Quality Settings
The download script automatically selects:
- Best MP4 format available
- Maximum 720p resolution (good quality, reasonable file size)
- Web-compatible codec

### 4. SEO and Accessibility
- Always provide meaningful `title` attributes
- Use `description` for important context
- The shortcode includes proper structured data

## Troubleshooting

### Video Not Loading
1. Check browser console for errors
2. Verify video files exist in `static/videos/`
3. Test video URLs manually

### YouTube Blocked
The shortcode automatically detects when YouTube is blocked and shows local fallback.

### Large File Sizes
Consider:
- Using 480p quality for longer videos: modify download script
- Compressing videos with ffmpeg
- Using external hosting for very large files

## Example Integration

Here's how you might add a video to your Gilbert cell project:

```markdown
---
title: "Gilbert Cell Mixer Design"
# ... other frontmatter
---

## Circuit Simulation Results

The following video demonstrates the Gilbert cell operation:

{{< video 
    youtube="your-simulation-video-id"
    local="/videos/gilbert-cell-simulation.mp4"
    title="Gilbert Cell Mixer Simulation"
    description="SPICE simulation showing conversion gain and frequency response"
    height="500px" >}}

## Layout Walkthrough

{{< video 
    youtube="your-layout-video-id"
    local="/videos/gilbert-cell-layout.mp4"
    title="Physical Layout Design Process"
    description="Step-by-step layout design in Magic VLSI" >}}
```

## Automation Ideas

### Automatic Backup Script
Create a cron job to periodically check and download videos:

```bash
# Add to crontab (crontab -e)
0 2 * * 0 cd /path/to/website && python scripts/download_videos.py --batch-file video_list.txt
```

### CI/CD Integration
Add video downloading to your deployment pipeline to ensure backups are always current.

## Legal Considerations

- Ensure you have rights to download and redistribute videos
- For academic use, consider fair use provisions
- When in doubt, contact video creators for permission
- Always provide proper attribution

## Alternative Solutions

If this approach doesn't fit your needs:

1. **Self-hosted video platform**: Use solutions like PeerTube
2. **Academic video repositories**: Upload to institutional repositories
3. **Cloud storage**: Use cloud providers with CDN integration
4. **Streaming services**: Consider academic-friendly platforms like Kaltura

---

*This guide ensures your academic content remains accessible for future researchers and students, regardless of external platform changes.*