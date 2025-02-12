import csv
import os

import utilities

file_name_clients_data = "clients_data.csv"
file_path_clients_data = "resources/" + file_name_clients_data

file_name_unavailable_time = "unavailable_time.csv"
file_path_unavailable_time = "resources/" + file_name_unavailable_time


def add_header(file_name):
    if file_name == "clients_data.csv":
        return "user_id", "name", "phone_number", "services", "book_date", "book_time"
    else:
        return "date", "time"


def create_csv_file(file_path, file_name):
    if not os.path.isfile(file_path):
        with open(file_path, "w", newline="") as stream:
            writer = csv.writer(stream)
            header = add_header(file_name)
            writer.writerow(header)


def client_to_tuple(client):
    return client.client_id, client.name, client.phone_number, client.services, client.book_date, client.book_time


def add_book_client(client):
    with open(file_path_clients_data, "a", encoding='utf-8', newline="") as stream:
        writer = csv.writer(stream)
        row = client_to_tuple(client)
        writer.writerow(row)


def time_to_tuple(client):
    return client.book_date, utilities.generate_book_time(client.book_time)


def add_book_time(client):
    with open(file_path_unavailable_time, "a", encoding='utf-8', newline="") as stream:
        writer = csv.writer(stream)
        row = time_to_tuple(client)
        writer.writerow(row)
