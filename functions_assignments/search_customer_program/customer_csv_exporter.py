class CustomerCsvExporter:
    def convert_to_csv(self, customers):
        lines = []
        for customer in customers:
            lines.append(
                f"{customer.customer_id},"
                f"{customer.company_name},"
                f"{customer.contact_name},"
                f"{customer.country}"
            )
        return "\n".join(lines)
