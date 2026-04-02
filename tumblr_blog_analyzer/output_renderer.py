class OutputRenderer:
    """Responsible for displaying results"""

    def show_blog_info(self, info):
        """Displays blog information"""
        print("\n")
        print(f"title: {info['title']}")
        print(f"name: {info['name']}")
        print(f"description: {info['description']}")
        print(f"no of post: {info['post_count']}")
        print("\n")

    def show_photo_urls(self, photo_data):
        """Displays photo URLs"""
        for post_number, urls in photo_data.items():
            print(f"{post_number}. {urls[0]}")
            for extra_url in urls[1:]:
                print(f"   {extra_url}")
