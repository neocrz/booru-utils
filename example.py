from bd import AibooruDownloader, DanbooruDownloader


urls = [
    "https://aibooru.online/posts/50789",
    # Add more URLs as needed
]

# Create a single instance of BooruDownloader
downloader = AibooruDownloader()

# Process each URL
for url in urls:
    downloader.fetch_json_data(url)
    downloader.see_tag_string()
    downloader.download_img_and_tag_string()



urls = [
    "https://danbooru.donmai.us/posts/6904790",
]

downloader = DanbooruDownloader()

# Process each URL
for url in urls:
    downloader.fetch_json_data(url)
    downloader.see_tag_string()
    downloader.download_img_and_tag_string()