import pickle

class BookRepository:
    def save(self, book):
        filename = f"/documents/{book.get_title()} - {book.get_author()}"
        with open(filename, "wb") as file:
            pickle.dump(book, file)
