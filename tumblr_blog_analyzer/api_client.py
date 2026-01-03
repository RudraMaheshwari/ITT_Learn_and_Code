import requests
import json

class TumblrApiClient:
    """Handles communication with Tumblr API v1"""

    BASE_API_URL = "https://{blog}.tumblr.com/api/read/json"

    def __init__(self):
        """Initialize with default API parameters"""
        self.default_params = {
            "type": "photo"
        }

    def fetch_blog_data(self, blog_name, start, count):
        """Fetches blog data from Tumblr API"""
        params = {
            **self.default_params,
            "start": start,
            "num": count
        }

        response = requests.get(
            self.BASE_API_URL.format(blog=blog_name),
            params=params
        )

        json_text = response.text
        if json_text.startswith("var tumblr_api_read = "):
            json_text = json_text[len("var tumblr_api_read = "):]

        return json_text.rstrip().rstrip(";")

    def parse_response(self, json_text):
        """Parses JSON response from Tumblr API"""
        return json.loads(json_text)

    def extract_blog_info(self, data):
        """Extracts blog information from parsed data"""
        return {
            "title": data["tumblelog"]["title"],
            "name": data["tumblelog"]["name"],
            "description": data["tumblelog"]["description"],
            "post_count": data["posts-total"]
        }

    def extract_photo_urls(self, posts, start_index):
        """Extracts photo URLs from parsed data"""
        photo_results = {}
        post_number = start_index

        for post in posts:
            image_urls = []

            if "photos" in post:
                for photo in post["photos"]:
                    image_urls.append(photo["photo-url-1280"])

            if image_urls:
                photo_results[post_number] = image_urls

            post_number += 1

        return photo_results
