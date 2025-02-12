class Client:
    client_id: int
    name: str
    phone_number: str
    services: str
    book_date: str
    book_time: str

    def set_client_id(self, client_id):
        self.client_id = client_id

    def get_client_id(self):
        return self.client_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number

    def get_phone_number(self):
        return self.phone_number

    def set_services(self, services):
        self.services = services

    def get_services(self):
        return self.services

    def set_book_date(self, date):
        self.book_date = date

    def get_book_date(self):
        return self.book_date

    def set_book_time(self, time):
        self.book_time = time

    def get_book_time(self):
        return self.book_time
