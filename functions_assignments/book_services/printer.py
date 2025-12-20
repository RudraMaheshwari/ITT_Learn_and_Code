class Printer(ABC):
    @abstractmethod
    def print_page(self, page):
        pass

class PlainTextPrinter(Printer):
    def print_page(self, page):
        print(page)

class HtmlPrinter(Printer):
    def print_page(self, page):
        print(f'<div style="single-page">{page}</div>')
