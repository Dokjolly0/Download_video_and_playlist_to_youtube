import yt_dlp
import os

def download_video_subtitles(url, subtitles_lang=None, output_dir="./downloads"):
    """
    Scarica i sottotitoli di un singolo video, mantenendo lo stesso nome del video.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Crea la cartella se non esiste

    # Imposta il template di output per mantenere il nome del video
    ydl_opts = {
        'writesubtitles': True,  # Abilita il download dei sottotitoli
        'writeautomaticsub': True,  # Abilita i sottotitoli automatici (se disponibili)
        'subtitleslangs': subtitles_lang if subtitles_lang else [],  # Lingua dei sottotitoli (italiano, inglese, etc.)
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Salva con il nome del video
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_playlist(playlist_url, output_dir="./downloads", number_videos=False, subtitles_lang=None):
    """
    Scarica i video di una playlist e i sottotitoli per ogni video.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Crea la cartella se non esiste

    # Imposta il modello di output per la playlist con numerazione se richiesto
    outtmpl = f'{output_dir}/%(title)s.%(ext)s'
    if number_videos:
        outtmpl = f'{output_dir}/%(playlist_index)s. %(title)s.%(ext)s'

    # Opzioni per yt-dlp
    ydl_opts = {
        'outtmpl': outtmpl,  # Template di output
        'format': 'bestvideo+bestaudio/best',  # Seleziona il miglior formato video/audio disponibile
        'subtitleslangs': ['all'],  # Specifica di scaricare tutti i sottotitoli
        'writeautomaticsub': True,  # Scrivi i sottotitoli automatici
        'writesubtitles': True,  # Scrivi i sottotitoli disponibili
        'allsubs': True,  # Scarica tutti i sottotitoli (compresi quelli automatici)
        'merge_output_format': 'mkv',  # Unifica i formati in MKV (se desideri)
    }

    # Usa yt-dlp per ottenere i dettagli della playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            playlist_info = ydl.extract_info(playlist_url, download=False)
        except Exception as e:
            print(f"Errore nel recuperare la playlist: {e}")
            return

        print(f"Titolo della Playlist: {playlist_info.get('title')}")
        print(f"Numero di Video: {len(playlist_info.get('entries', []))}")
        print('-' * 50)

        total_videos = len(playlist_info.get('entries', []))
        for idx, video in enumerate(playlist_info.get('entries', []), start=1):
            print(f"Scaricando ({idx}/{total_videos}): {video.get('title')}")

            video_url = video.get('webpage_url') or video.get('url')
            if not video_url:
                print(f"Impossibile trovare l'URL per il video: {video.get('title')}")
                continue

            try:
                # Scarica il video e i sottotitoli (se disponibili)
                download_video_subtitles(video_url, subtitles_lang, output_dir)
            except Exception as e:
                print(f"Errore nel scaricare {video.get('title')}: {e}")

# Esempio di utilizzo:
playlist_url = "https://www.youtube.com/playlist?list=PL6lQzryxKYL8j3EvACvJPpAqXnwS3D43C"
output_dir = "./downloads"  # Cartella in cui verranno salvati i video e i sottotitoli
subtitles_lang = ["it", "eng"]  # Sottotitoli in italiano e inglese

# Chiama la funzione per scaricare la playlist con i sottotitoli
download_playlist(playlist_url, output_dir, number_videos=True, subtitles_lang=subtitles_lang)
