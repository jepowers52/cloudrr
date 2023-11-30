"""Customers at Hackbright."""


class Customer:
    """Ubermelon customer."""

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<Customer: {self.first_name} {self.last_name}>"


def read_customers_from_file(filepath):
    """Read customer data and populate dictionary of customers.

    Dictionary will be {id: Melon object}
    """

    customers_types = {}

    with open(filepath) as file:
        for line in file:
            (
                first_name,
                last_name,
                email,
                password
            ) = line.strip().split("|")

            customers_types[email] = Customer(
                first_name,
                last_name,
                email,
                password
            )

    return customers_types

def get_by_id(customer_email):
    """Return a customer, given its email."""

    return customers_types[customer_email]


customers_types = read_customers_from_file("customers.txt")