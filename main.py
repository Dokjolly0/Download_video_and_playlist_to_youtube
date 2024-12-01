from utils.utils import *
from utils.utils_youtube import *

def main():
    # root_path = get_root_path()
    # downloads_path = get_downloads_folder()
    # show_menu()
    # video_list = get_available_video_list("https://www.youtube.com/watch?v=hPVEBnNMWuU&list=PLG9LtUAxf1iNSTNq5mAzMUTzET9o7tTFu&index=1")
    # if video_list is not None:
    #     for video in video_list:
    #         print(video)
    pass

if __name__ == "__main__":
    main()


print(validate_youtube_url("https://www.youtube.com/watch?v=1234567890"))
print(validate_youtube_url("https://www.youtube.com/watch?v=hPVEBnNMWuU&list=PLG9LtUAxf1iNSTNq5mAzMUTzET9o7tTFu&index=1"))
print(validate_youtube_url("https://www.youtube.com/playlist?list=1234567890"))
print(validate_youtube_url("https://www.google.com"))