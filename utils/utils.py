import os
import sys
import re
from urllib.parse import urlparse, parse_qs


# ===========================
# Path Utilities
# ===========================
def get_root_path():
    """
    Ottiene il percorso della cartella principale del progetto.

    Returns:
        str: Il percorso della cartella principale.
    """
    try:
        if getattr(sys, 'frozen', False):  # Se l'app è eseguita da un eseguibile
            current_path = os.path.dirname(sys.executable)
        else:
            current_path = os.path.dirname(os.path.abspath(__file__))  # Modalità sviluppo
        root_path = os.path.dirname(current_path)
    except Exception as e:
        print(f"Error: {e}")
        return None

    print(f"Root folder: {root_path}")
    return root_path


def get_downloads_folder():
    """
    Ottiene il percorso della cartella 'downloads'. Se non esiste, la crea.

    Returns:
        str: Il percorso completo della cartella 'downloads'.
    """
    root_path = get_root_path()
    if root_path is None:
        return None

    downloads_path = os.path.join(root_path, "downloads")
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)

    return downloads_path


# ===========================
# YouTube URL Validation
# ===========================
def validate_youtube_url(url):
    """
    Classifica un URL di YouTube in base al tipo (video singolo, playlist, video in playlist)
    e restituisce un dizionario con le informazioni rilevanti.
    """
    # Verifica se l'URL è valido
    try:
        parsed_url = urlparse(url)
    except Exception:
        return {'valid': False, 'reason': 'URL non valido'}

    # Verifica dominio di YouTube
    if parsed_url.netloc not in ("www.youtube.com", "youtube.com", "youtu.be"):
        return {'valid': False, 'reason': 'URL non di YouTube'}

    # Estrai i parametri e il percorso
    query_params = parse_qs(parsed_url.query)
    path = parsed_url.path

    # Estrai l'ID del video dalla query o dal percorso
    video_id = None
    if 'v' in query_params:
        video_id = query_params['v'][0]
    elif re.match(r"^/[A-Za-z0-9_-]{11}$", path):
        video_id = path.strip('/')

    # Regole di classificazione
    if video_id:
        if 'list' in query_params:
            return {'valid': True, 'type': 'video_in_playlist', 'id': video_id}
        return {'valid': True, 'type': 'single_video', 'id': video_id}
    elif 'list' in query_params:
        playlist_id = query_params['list'][0]
        return {'valid': True, 'type': 'playlist', 'id': playlist_id}
    else:
        return {'valid': False, 'reason': 'URL non valido o conosciuto di YouTube'}


def get_type_url(validation_result):
    """
    Ottiene il tipo di URL da un risultato di validazione.

    Args:
        validation_result (dict): Il risultato della validazione.

    Returns:
        str: Il tipo di URL ('video', 'playlist', 'Errore').
    """
    if validation_result["valid"]:
        return validation_result["type"]

    print(f"Errore di ottenimento del tipo di video: {validation_result['reason']}")
    return validation_result["reason"]


def get_id_url(validation_result):
    """
    Ottiene l'ID dell'URL da un risultato di validazione.

    Args:
        validation_result (dict): Il risultato della validazione.

    Returns:
        str: L'ID dell'URL oppure None in caso di errore.
    """
    if validation_result["valid"]:
        return validation_result["id"]

    print(f"Errore di ottenimento dell'id: {validation_result['reason']}")
    return None


# ===========================
# Menu Interaction
# ===========================
def show_menu():
    """
    Mostra un menu all'utente per selezionare un'opzione.

    Returns:
        str: La scelta selezionata dall'utente.
    """
    while True:
        print("\nMenu:")
        print("1: Video playlist")
        print("2: Video")
        print("3: Audio playlist")
        print("4: Audio")
        print("5: Exit")

        choice = input("Seleziona un'opzione: ")
        available_choices = ['1', '2', '3', '4', '5']

        if choice not in available_choices:
            print("Scelta non valida")
            continue
        elif choice == '5':
            print("Uscita...")
            sys.exit()
        else:
            break
    return choice

