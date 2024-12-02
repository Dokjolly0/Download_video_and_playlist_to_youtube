import yt_dlp
import requests
import re  # Importa il modulo per le espressioni regolari
import os  # Per gestire i percorsi di file
import sys
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse  # Per manipolare gli URL

def clean_filename(filename):
    """Rimuove i caratteri non validi nei nomi dei file"""
    return re.sub(r'[\\/*?:"<>|]', '', filename)  # Rimuove i caratteri non validi

def modify_subtitle_url(url, target_lang):
    """Modifica il parametro `tlang` dell'URL per scaricare i sottotitoli nella lingua desiderata."""
    # Analizza l'URL in parti
    parsed_url = urlparse(url)
    # Estrai i parametri di query
    query_params = parse_qs(parsed_url.query)
    
    # Modifica il parametro 'tlang' con la lingua desiderata
    query_params['tlang'] = target_lang
    
    # Ricostruisci la query con il parametro modificato
    new_query = urlencode(query_params, doseq=True)
    
    # Ritorna l'URL modificato
    return urlunparse(parsed_url._replace(query=new_query))

def download_automatic_subtitle(url, target_langs=["it", "en"], print_info=False, folder_path="./downloads"):
    # Crea la cartella se non esiste
    os.makedirs(folder_path, exist_ok=True)
    
    # Impostazioni per yt-dlp
    ydl_opts = {
        'writeautomaticsub': True,  # Scarica i sottotitoli automatici se non ci sono sottotitoli reali
        'skip_download': True,      # Non scarica il video, solo i sottotitoli
        'outtmpl': '%(id)s.%(ext)s',  # Nome del file in base all'ID del video
        'subtitlesformat': 'best',   # Usa il miglior formato disponibile per i sottotitoli
        'quiet': True,  # Silenzia le stampe di log generali
    }

    try:
        # Crea l'oggetto yt-dlp con le opzioni di configurazione
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)  # Ottieni le informazioni del video
            requested_subtitles = info_dict.get('requested_subtitles', {})  # Estrai i sottotitoli disponibili
            
            if print_info:
                print("Lingue disponibili:", ', '.join(requested_subtitles.keys()))

            video_title = clean_filename(info_dict['title'])  # Pulisci il titolo del video per il nome del file

            # Estrai l'URL originale del sottotitolo disponibile (ad esempio, in inglese)
            original_url = None
            if 'en' in requested_subtitles:
                original_url = requested_subtitles['en']['url']

            if not original_url:
                print("Nessun sottotitolo disponibile. Uscendo.")
                return

            # Scarica i sottotitoli per ogni lingua richiesta, modificando l'URL
            for lang in target_langs:
                # Modifica l'URL per la lingua richiesta
                subtitle_url = modify_subtitle_url(original_url, lang)
                subtitle_ext = requested_subtitles.get('en', {}).get('ext', 'vtt')  # Estrai l'estensione del sottotitolo (assumendo 'en' come esempio)
                subtitle_name = f"{video_title}.{lang}.{subtitle_ext}"  # Nome file

                if print_info:
                    print(f"Scaricando sottotitoli ({lang}): {subtitle_url}")
                
                # Esegui la richiesta per ottenere il sottotitolo
                response = requests.get(subtitle_url)
                if response.status_code == 200:
                    subtitle_path = os.path.join(folder_path, subtitle_name)
                    with open(subtitle_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Sottotitolo salvato in: {subtitle_path}")
                else:
                    print(f"Errore nel download del sottotitolo in {lang}.", file=sys.stderr)

    except Exception as e:
        print(f"Si è verificato un errore: {e}", file=sys.stderr)

# # Esempio di utilizzo:
# url_video = "https://www.youtube.com/watch?v=CDQ_dLmDbDo"
# download_automatic_subtitle(url_video, target_langs=["it", "en", "es"], print_info=True, folder_path="./downloads")
