from adjacent_country_finder import AdjacentCountryFinder

class AdjacentCountryConsole:
    def __init__(self):
        self.country_finder = AdjacentCountryFinder()

    def run_program(self):
        print("=== Adjacent Country Finder ===")
        country_code = input("Enter Country Code (e.g., IN, US, NZ): ").strip()
        self.country_finder.display_adjacent_countries(country_code)
