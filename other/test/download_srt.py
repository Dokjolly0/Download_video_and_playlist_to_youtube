import yt_dlp

def download_subtitles(url):
    ydl_opts = {
        'writesubtitles': True,  # Abilita il download dei sottotitoli
        'writeautomaticsub': True,  # Abilita il download dei sottotitoli automatici (se disponibili)
        'subtitleslangs': ['it'],  # Scarica i sottotitoli in italiano (puoi cambiare la lingua se necessario)
        'outtmpl': '%(id)s.%(ext)s',  # Modello di output per il nome del file
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# URL del video YouTube
video_url = 'https://www.youtube.com/watch?v=YCIycqCXGo8'

download_subtitles(video_url)
