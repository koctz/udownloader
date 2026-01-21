import yt_dlp
import asyncio
import os

def get_video_info(url):
    ydl_opts = {'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = []
        # Фильтруем форматы, где есть видео + аудио в одном файле
        seen_res = set()
        for f in info.get('formats', []):
            res = f.get('height')
            if res and res not in seen_res and f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                formats.append({'id': f['format_id'], 'res': res, 'ext': f['ext']})
                seen_res.add(res)
        return info.get('title', 'Video'), sorted(formats, key=lambda x: x['res'], reverse=True)

async def download_video(url, format_id):
    output_filename = f"downloads/%(title)s_{format_id}.%(ext)s"
    ydl_opts = {
        'format': format_id,
        'outtmpl': output_filename,
        'quiet': True,
    }
    
    def sync_download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)

    return await asyncio.to_thread(sync_download)
