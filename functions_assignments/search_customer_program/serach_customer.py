class CustomerSearch:
    def __init__(self, database):
        self.database = database

    def search_by_country(self, country):
        return self._search(lambda customer: country in customer.country)

    def search_by_company_name(self, company_name):
        return self._search(lambda customer: company_name in customer.company_name)

    def search_by_contact_name(self, contact_name):
        return self._search(lambda customer: contact_name in customer.contact_name)

    def _search(self, condition):
        return sorted(
            filter(condition, self.database.customers),
            key=lambda customer: customer.customer_id
        )
