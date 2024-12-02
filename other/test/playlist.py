import yt_dlp
import os
from utils.download_subtitle import download_automatic_subtitle

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
        'quiet': True,  # Disabilita il progresso del download
        'outtmpl': outtmpl,  # Modello di output per il nome e la cartella del file
        'writesubtitles': True,  # Abilita il download dei sottotitoli
        'subtitleslangs': subtitles_lang if subtitles_lang else [],  # Lingue dei sottotitoli
    }

    # Usa yt-dlp per ottenere i dettagli della playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            playlist_info = ydl.extract_info(playlist_url, download=False)
        except Exception as e:
            print(f"Errore nel recuperare la playlist: {e}")
            return

        total_videos = len(playlist_info.get('entries', []))
        for idx, video in enumerate(playlist_info.get('entries', []), start=1):
            video_url = video.get('webpage_url') or video.get('url')
            if not video_url:
                print(f"Errore: Impossibile trovare l'URL per il video (indice {idx})")
                continue

            try:
                # Scarica il video e i sottotitoli (se disponibili)
                download_automatic_subtitle(video_url, True)
            except Exception as e:
                print(f"Errore nel scaricare video all'indice {idx}: {e}")

# Esempio di utilizzo:
playlist_url = "https://www.youtube.com/playlist?list=PL6lQzryxKYL8j3EvACvJPpAqXnwS3D43C"
output_dir = "./downloads"  # Cartella in cui verranno salvati i video e i sottotitoli
subtitles_lang = ["it", "eng"]  # Sottotitoli in italiano e inglese

# Chiama la funzione per scaricare la playlist con i sottotitoli
download_playlist(playlist_url, output_dir, number_videos=True, subtitles_lang=subtitles_lang)
