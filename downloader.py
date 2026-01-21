import yt_dlp
import asyncio
import os

async def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    def sync_extract():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    
    return await asyncio.to_thread(sync_extract)

async def download_video(url, format_id):
    # Эта строка должна иметь отступ (4 пробела)
    output_filename = os.path.join("downloads", f"%(title)s_{format_id}.%(ext)s")
    
    ydl_opts = {
        'format': f"{format_id}+bestaudio/best",
        'outtmpl': output_filename,
        'merge_output_format': 'mp4',
        'extractor_args': {
            'youtube': {
                'po_token': ['web+http://pot_provider:8080/token'],
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    
    def sync_download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)

    return await asyncio.to_thread(sync_download)
