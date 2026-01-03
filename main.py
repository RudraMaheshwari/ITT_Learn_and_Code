from tumblr_blog_analyzer.api_client import TumblrApiClient
from tumblr_blog_analyzer.input_handler import UserInputHandler
from tumblr_blog_analyzer.output_renderer import OutputRenderer

class TumblrApplication:
    """Coordinates the complete Tumblr blog analysis"""

    def start_application(self):
        input_handler = UserInputHandler()
        api_client = TumblrApiClient()
        renderer = OutputRenderer()

        blog_name = input_handler.read_blog_name()
        start, end = input_handler.read_post_range()

        start_index = start - 1
        count = end - start + 1

        raw_json = api_client.fetch_blog_data(blog_name, start_index, count)
        parsed_data = api_client.parse_response(raw_json)

        blog_info = api_client.extract_blog_info(parsed_data)
        renderer.show_blog_info(blog_info)

        photo_urls = api_client.extract_photo_urls(parsed_data["posts"], start)
        renderer.show_photo_urls(photo_urls)

if __name__ == "__main__":
    TumblrApplication().start_application()
