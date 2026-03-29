class AdjacentCountryFinder:
    ADJACENT_COUNTRIES = {
        "IN": ["Pakistan", "China", "Nepal", "Bhutan", "Bangladesh", "Myanmar"],
        "US": ["Canada", "Mexico"],
        "CA": ["United States"],
        "MX": ["United States", "Guatemala", "Belize"],
        "NZ": [],
        "AU": [],
        "FR": ["Belgium", "Luxembourg", "Germany", "Switzerland", "Italy", "Spain", "Monaco", "Andorra"],
        "DE": ["Denmark", "Poland", "Czech Republic", "Austria", "Switzerland", "France", "Belgium", "Netherlands", "Luxembourg"]
    }

    def get_adjacent_countries(self, country_code: str):
        country_code = country_code.upper()
        if country_code not in self.ADJACENT_COUNTRIES:
            return None
        return self.ADJACENT_COUNTRIES[country_code]

    def display_adjacent_countries(self, country_code: str):
        adjacent_list = self.get_adjacent_countries(country_code)
        if adjacent_list is None:
            print(f"Invalid country code: {country_code}")
        elif len(adjacent_list) == 0:
            print(f"{country_code} has no adjacent countries.")
        else:
            print(f"Adjacent countries to {country_code}:")
            for country in adjacent_list:
                print(f"- {country}")