from pytube import YouTube
from pytube.contrib.playlist import Playlist
import os
import sys
from pytube.exceptions import VideoUnavailable, PytubeError
import time

def get_available_video(video):
    streams = video.streams.filter(file_extension='mp4')
    available_video = []
    for stream in streams:
        if stream.resolution:
            available_video.append((stream.resolution, stream))
    available_video = sorted(available_video, key=lambda x: int(x[0][:-1]))
    return available_video

def get_available_audio(video):
    streams = video.streams.filter(only_audio=True, file_extension='mp4')
    available_audio = []
    for stream in streams:
        available_audio.append((stream.abr, stream))
    available_audio = sorted(available_audio, key=lambda x: int(x[0][:-4]))
    return available_audio

def on_progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f'Download progress: {percentage:.2f}%', end='\r')

def download_video(video, resolution, output_folder):
    retries = 5
    for attempt in range(retries):
        try:
            if resolution == 'highest':
                stream = video.streams.filter(file_extension='mp4', resolution=None).order_by('resolution').desc().first()
            else:
                stream = video.streams.filter(res=resolution, file_extension='mp4').first()

            if stream:
                print(f"Downloading: {video.title}")
                stream.download(output_path=output_folder)
                print(f"Video scaricato: {video.title} in {stream.resolution}\n")
                print("Path: " + output_folder)
            else:
                print(f"Risoluzione {resolution} non disponibile per {video.title}. Download nella qualità più alta trovata.")
                best_stream = video.streams.filter(file_extension='mp4', resolution=None).order_by('resolution').desc().first()
                best_stream.download(output_path=output_folder)
                print(f"\nVideo scaricato: {video.title} in {best_stream.resolution}")
            return True
        except VideoUnavailable:
            print(f"Il video {video.title} non è disponibile.")
            return False
        except Exception as e:
            print(f"Errore nel download di {video.title}: {e}. Tentativo {attempt + 1} di {retries}.")
            if attempt < retries - 1:
                time.sleep(5)  # Wait before retrying
    print(f"Fallito il download di {video.title} dopo {retries} tentativi.")
    return False

def download_audio(video, audio_quality, output_folder):
    retries = 5
    for attempt in range(retries):
        try:
            if audio_quality == 'highest':
                stream = video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
            else:
                stream = video.streams.filter(abr=audio_quality, only_audio=True, file_extension='mp4').first()

            if stream:
                print(f"Downloading: {video.title}")
                stream.download(output_path=output_folder, filename=video.title + ".mp3")
                print(f"Audio scaricato: {video.title} in {stream.abr}\n")
            else:
                print(f"Qualità audio {audio_quality} non disponibile per {video.title}. Download nella qualità più alta trovata.")
                best_stream = video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
                best_stream.download(output_path=output_folder, filename=video.title + ".mp3")
                print(f"\nAudio scaricato: {video.title} in {best_stream.abr}")
            return True
        except VideoUnavailable:
            print(f"Il video {video.title} non è disponibile.")
            return False
        except Exception as e:
            print(f"Errore nel download di {video.title}: {e}. Tentativo {attempt + 1} di {retries}.")
            if attempt < retries - 1:
                time.sleep(5)  # Wait before retrying
    print(f"Fallito il download di {video.title} dopo {retries} tentativi.")
    return False

def validate_input_url(url):
    try:
        if 'playlist' in url.lower():
            return 'playlist'
        else:
            YouTube(url)
            return 'video'
    except Exception as e:
        print(f"Errore nella validazione dell'URL: {e}")
        return None

def main():
    try:
        if getattr(sys, 'frozen', False):
            # Se l'applicazione è in modalità "frozen" (cioè è stata trasformata in un eseguibile)
            current_path = os.path.dirname(sys.executable)
        else:
            # Se l'applicazione è in modalità "non-frozen" (cioè è in esecuzione come script Python)
            current_path = os.path.dirname(os.path.abspath(__file__))
        
        output_folder = os.path.join(current_path, "yt_download")
        #print(f"Cartella di output: {output_folder}")
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        while True:
            print("\nMenu:")
            print("1: Video playlist")
            print("2: Video")
            print("3: Audio playlist")
            print("4: Audio")
            print("5: Exit")
            choice = input("Seleziona un'opzione: ")

            if choice == '5':
                print("Uscita...")
                break

            input_url = input("Inserisci l'url del video o di una playlist: ")
            url_type = validate_input_url(input_url)
            failed_downloads = []

            if url_type == 'playlist':
                try:
                    playlist = Playlist(input_url)
                    if len(playlist.video_urls) == 0:
                        print("La playlist non contiene video.")
                        continue
                except PytubeError as e:
                    print("Errore: La playlist è privata o non disponibile.")
                    continue

                total_videos = len(playlist.video_urls)
                print(f"\nTrovati {total_videos} video nella playlist.")

                if choice == '1':
                    # Ask for video quality selection
                    valid_selection = False
                    while not valid_selection:
                        available_streams = get_available_video(YouTube(playlist.video_urls[0]))
                        print("\nRisoluzione disponibile:")
                        print("0: Massima qualità")
                        for i, (resolution, _) in enumerate(available_streams):
                            print(f"{i + 1}: {resolution}")
                        selection = int(input("Seleziona la qualità per il download (Esempio: 2 per 1080p, 1 per 720p, 0 per massima qualità...): ")) - 1
                        if selection == -1:
                            resolution = 'highest'
                            valid_selection = True
                        elif 0 <= selection < len(available_streams):
                            resolution = available_streams[selection][0]
                            valid_selection = True
                        else:
                            print("Scelta non valida. Riprova.")

                    for video_url in playlist.video_urls:
                        video = YouTube(video_url, on_progress_callback=on_progress_callback)
                        success = download_video(video, resolution, output_folder)
                        if not success:
                            failed_downloads.append(video.title)
                        total_videos -= 1
                        if total_videos > 0:
                            print(f"Video rimanenti da scaricare: {total_videos}")
                        elif(total_videos == 0):
                            print("Hai scaricato tutti i video.")

                elif choice == '3':
                    # Ask for audio quality selection
                    valid_selection = False
                    while not valid_selection:
                        available_streams = get_available_audio(YouTube(playlist.video_urls[0]))
                        print("\nQualità audio disponibile:")
                        print("0: Massima qualità")
                        for i, (audio_quality, _) in enumerate(available_streams):
                            print(f"{i + 1}: {audio_quality}")
                        selection = int(input("Seleziona la qualità per il download (Esempio: 2 per 128kbps, 1 per 160kbps, 0 per massima qualità...): ")) - 1
                        if selection == -1:
                            audio_quality = 'highest'
                            valid_selection = True
                        elif 0 <= selection < len(available_streams):
                            audio_quality = available_streams[selection][0]
                            valid_selection = True
                        else:
                            print("Scelta non valida. Riprova.")

                    for video_url in playlist.video_urls:
                        video = YouTube(video_url, on_progress_callback=on_progress_callback)
                        success = download_audio(video, audio_quality, output_folder)
                        if not success:
                            failed_downloads.append(video.title)
                        total_videos -= 1
                        print(f"Video rimanenti da scaricare: {total_videos}")

            elif url_type == 'video':
                video = YouTube(input_url, on_progress_callback=on_progress_callback)

                if choice == '2':
                    # Ask for video quality selection
                    resolution = None
                    valid_selection = False
                    while not valid_selection:
                        available_streams = get_available_video(video)
                        print("\nRisoluzione disponibile:")
                        print("0: Massima qualità")
                        for i, (resolution, _) in enumerate(available_streams):
                            print(f"{i + 1}: {resolution}")
                        selection = int(input("Seleziona la qualità per il download (Esempio: 2 per 1080p, 1 per 720p, 0 per massima qualità...): ")) - 1
                        if selection == -1:
                            resolution = 'highest'
                            valid_selection = True
                        elif 0 <= selection < len(available_streams):
                            resolution = available_streams[selection][0]
                            valid_selection = True
                        else:
                            print("Scelta non valida. Riprova.")

                    success = download_video(video, resolution, output_folder)
                    if not success:
                        failed_downloads.append(video.title)

                elif choice == '4':
                    # Ask for audio quality selection
                    audio_quality = None
                    valid_selection = False
                    while not valid_selection:
                        available_streams = get_available_audio(video)
                        print("\nQualità audio disponibile:")
                        print("0: Massima qualità")
                        for i, (audio_quality, _) in enumerate(available_streams):
                            print(f"{i + 1}: {audio_quality}")
                        selection = int(input("Seleziona la qualità per il download (Esempio: 2 per 128kbps, 1 per 160kbps, 0 per massima qualità...): ")) - 1
                        if selection == -1:
                            audio_quality = 'highest'
                            valid_selection = True
                        elif 0 <= selection < len(available_streams):
                            audio_quality = available_streams[selection][0]
                            valid_selection = True
                        else:
                            print("Scelta non valida. Riprova.")

                    success = download_audio(video, audio_quality, output_folder)
                    if not success:
                        failed_downloads.append(video.title)

            else:
                print("URL non valido o opzione non valida. Inserisci un URL valido e seleziona un'opzione valida.")

            if failed_downloads:
                print("\nDownload falliti per i seguenti video:")
                for title in failed_downloads:
                    print(title)

    except KeyboardInterrupt:
        print("\nInterruzione da tastiera rilevata. Uscita dal programma...")

if __name__ == "__main__":
    main()

#https://www.youtube.com/playlist?list=PLG9LtUAxf1iNSTNq5mAzMUTzET9o7tTFu
