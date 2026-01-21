import yt_dlp

def get_video_info(url):
    ydl_opts = {'quiet': True, 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = []
        # Выбираем только форматы с видео и аудио вместе для простоты
        for f in info.get('formats', []):
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                formats.append({
                    'format_id': f['format_id'],
                    'resolution': f.get('height', 'unknown'),
                    'ext': f['ext']
                })
        return info.get('title'), formats
