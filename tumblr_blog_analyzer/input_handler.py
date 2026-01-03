class UserInputHandler:
    """Reads and validates user input"""

    def read_blog_name(self):
        """Reads Tumblr blog name from user input"""
        return input("enter the Tumblr blog name:\n").strip()

    def read_post_range(self):
        """Reads post range from user input"""
        while True:
            try:
                user_input = input("enter the range (e.g., 1-10):\n").strip()
                start, end = user_input.split("-")
                return int(start), int(end)
            except ValueError:
                print("Invalid format. Please enter range like '1-10'.")
