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
    output_filename = os.path.join("downloads", f"%(title)s_{format_id}.%(ext)s")
    
    ydl_opts = {
        'format': f"{format_id}+bestaudio/best",
        'outtmpl': output_filename,
        'merge_output_format': 'mp4',
        # Настройка использования прокси-генератора токенов
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

    return await asyncio.to_thread(sync_download)
