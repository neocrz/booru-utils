import urllib.parse
import requests
import urllib.request
from urllib.request import urlretrieve
import time

class BooruBase:
    def __init__(self):
        self.url = None
        self.data = None
        self.tag_string = None
        self.md5_value = None
        self.image_url = None

    def fetch_json_data(self, url):
        # Parse the URL to remove the query parameters
        parsed_url = urllib.parse.urlparse(url)
        new_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "", ""))

        # Add ".json" to the URL
        json_url = new_url + ".json"

        # Fetch the JSON data
        response = requests.get(json_url)
        self.data = response.json()
        self.url = url
    
    def see_tag_string(self):
        # Extract the value of the 'tag_string' key
        self.tag_string = self.data.get('tag_string', None)
        print(f"Content of the 'tag_string' key for URL {self.url}:", self.tag_string)

class DanbooruDownloader(BooruBase):
    def download_img_and_tag_string(self):
        # Extract the value of the 'md5' key
        self.md5_value = self.data.get('md5', None)

        # Find the variant with type "sample" in ["media_asset"]["variants"]
        sample_variant = next((variant for variant in self.data["media_asset"]["variants"] if variant["type"] == "sample"), None)

        if sample_variant:
            # Extract the URL of the image
            self.image_url = sample_variant.get("url", None)

            if self.image_url:
                # Retry downloading the image in case of an error
                max_retries = 3
                for _ in range(max_retries):
                    try:
                        # Download the image with the name of md5 + file extension
                        file_extension = self.image_url.split('.')[-1]
                        image_filename = f"{self.md5_value}.{file_extension}" if self.md5_value else "downloaded_image.jpg"
                        urlretrieve(self.image_url, image_filename)
                        print(f"Image downloaded successfully. Saved as {image_filename}")

                        # Save the 'tag_string' to a text file with the name of md5
                        if self.md5_value:
                            txt_filename = f"{self.md5_value}.txt"
                            with open(txt_filename, 'w') as txt_file:
                                txt_file.write(self.tag_string)
                            print(f"Tag string saved to {txt_filename}")

                        # Break out of the loop if download is successful
                        break
                    except Exception as e:
                        print(f"Error downloading image: {e}")
                        print("Retrying after 0.5 seconds...")
                        time.sleep(0.5)
                else:
                    print("Max retries reached. Download failed.")
            else:
                print("No image URL found.")
        else:
            print("No sample variant found in the JSON data.")
    

class AibooruDownloader(BooruBase):
    def download_img_and_tag_string(self):
        # Extract the value of the 'md5' key
        self.md5_value = self.data.get('md5', None)

        # Extract the URL of the image
        self.image_url = self.data.get('large_file_url', None)
        print(self.image_url)
        if self.image_url:
            # Retry downloading the image in case of an error
            max_retries = 3
            for _ in range(max_retries):
                try:
                    # Download the image with the name of md5 + file extension
                    file_extension = self.image_url.split('.')[-1]
                    image_filename = f"{self.md5_value}.{file_extension}" if self.md5_value else "downloaded_image.jpg"

                    # Create a request with headers
                    request = urllib.request.Request(self.image_url, headers={'User-Agent': 'Mozilla/5.0'})
                    
                    # Open the URL with the request
                    with urllib.request.urlopen(request) as response, open(image_filename, 'wb') as out_file:
                        # Copy the content of the response to the file
                        out_file.write(response.read())

                    print(f"Image downloaded successfully. Saved as {image_filename}")

                    # Save the 'tag_string' to a text file with the name of md5
                    if self.md5_value:
                        txt_filename = f"{self.md5_value}.txt"
                        with open(txt_filename, 'w') as txt_file:
                            txt_file.write(self.tag_string)
                        print(f"Tag string saved to {txt_filename}")

                    # Break out of the loop if download is successful
                    break
                except Exception as e:
                    print(f"Error downloading image: {e}")
                    print("Retrying after 0.5 seconds...")
                    time.sleep(0.5)
            else:
                print("Max retries reached. Download failed.")
        else:
            print("No image URL found.")