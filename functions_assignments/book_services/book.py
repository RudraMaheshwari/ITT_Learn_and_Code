class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.current_page = 0

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def turn_page(self):
        self.current_page += 1

    def get_current_page(self):
        return "current page content"
