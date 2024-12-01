import pytube

url = "https://www.youtube.com/playlist?list=PLG9LtUAxf1iNSTNq5mAzMUTzET9o7tTFu"
playlist = pytube.Playlist(url)

title_playlist = playlist.title
urls = playlist.video_urls

for url in urls:
    yt = pytube.YouTube(url)
    print(str(yt.captions.get_by_language_code("it")))












#url = 'https://www.youtube.com/watch?v=hPVEBnNMWuU&list=PLG9LtUAxf1iNSTNq5mAzMUTzET9o7tTFu&index=1'