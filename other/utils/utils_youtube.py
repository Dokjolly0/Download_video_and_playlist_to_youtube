import time
from pytube import YouTube
from pytube.contrib.playlist import Playlist
from pytube.exceptions import VideoUnavailable


def get_available_video_list(url):
    """
    Ottiene l'elenco dei flussi video disponibili per un URL di YouTube.

    Args:
        url (str): L'URL del video di YouTube.

    Returns:
        list: Un elenco di dizionari con dettagli dei flussi video disponibili.
              Ogni dizionario contiene 'itag', 'resolution', 'fps', e 'mime_type'.
              In caso di errore, ritorna None.
    """
    try:
        # Inizializza l'oggetto YouTube
        yt = YouTube(url)

        # Ottieni i flussi video
        streams = yt.streams.filter(only_video=True).order_by('resolution').desc()

        # Costruisci l'elenco dei dettagli dei flussi video
        video_list = []
        for stream in streams:
            video_list.append({
                "itag": stream.itag,
                "resolution": stream.resolution,
                "fps": stream.fps,
                "mime_type": stream.mime_type
            })

        return video_list

    except VideoUnavailable:
        print("Il video non è disponibile.")
        return None
    except Exception as e:
        print(f"Errore durante il recupero dei flussi video: {e}")
        return None