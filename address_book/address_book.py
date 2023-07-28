from prettytable import PrettyTable
from collections import UserDict
from datetime import datetime
import pickle
import re
from abc import ABC, abstractmethod


tutorial = '''
Adding instruction:
  name - no more than three words
  phones - can be several (each must contain 10 to 12 digits), enter with a space
  emails - can be several, enter with a space
  birthday - date in format dd/mm/yyyy (must be only one)
  address - must contain street and house number, all elements must be separated by a slash and start with a slash (example: /Country/City/Street/House)
'''


def get_valid_input(prompt, pattern=None):
    while True:
        value = input(prompt).strip()
        if pattern and not re.match(pattern, value):
            print("Invalid input. Please try again.")
            continue
        return value


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.Name.name] = record
        return "Done!"

    def delete_record(self, name):
        if name in self.data:
            self.data.pop(name)
            return "Done!"
        else:
            return "Contact not found!"

    def find(self, piece_of_info):
        result = []
        for name, record in self.data.items():
            contact_info = f"{name} {record.Phones.phone} {record.Emails.email} {record.Birthday.birthday[0] if record.Birthday.birthday else ''} {record.Address.address[0] if record.Address.address else ''}"
            if piece_of_info.lower() in contact_info.lower():
                result.append(contact_info)
        return result

    def load_address_book_from_txt(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    name, phones, birthday, emails, address = self._parse_record_from_txt(
                        line.strip())
                    self.add_record(Record(Name(name), Phone(phones),
                                           Birthday(birthday), Email(emails), Address(address)))
            print("Address book data loaded from txt file.")
        except FileNotFoundError:
            print("File not found. Creating a new AddressBook.")
            self.data = {}

    def _format_record_to_txt(self, record):
        name = record.Name.name
        phones = " ".join(record.Phones.phone)
        birthday = record.Birthday.birthday[0] if record.Birthday.birthday else ''
        emails = " ".join(record.Emails.email)
        address = " ".join(record.Address.address)
        return f"{name} | {phones} | {birthday} | {emails} | {address}"

    def _parse_record_from_txt(self, data):
        data = data.split(" | ")
        name = data[0]
        phones = data[1].split()
        birthday = [data[2]] if data[2] else []
        emails = data[3].split()
        address = data[4].split()
        return name, phones, birthday, emails, address

    def show_all(self):
        return list(self.data.values())

    def days_to_birthday(self, name):
        if name in self.data:
            return self.data[name].days_to_birthday()
        else:
            return "Contact not found!"

    def contacts_in_days(self, days):
        result = []
        for name, record in self.data.items():
            days_to_birthday = record.days_to_birthday()
            if days_to_birthday.startswith("In"):
                days_left = int(days_to_birthday.split()[1])
                if days_left <= days:
                    result.append(name)
        return result


class Record:
    def __init__(self, name, phones=None, birthday=None, emails=None, address=None):
        self.Name = name
        self.Phones = phones or Phone()
        self.Birthday = birthday or Birthday()
        self.Emails = emails or Email()
        self.Address = address or Address()

    def add_phone(self, phone):
        self.Phones.phone.extend(phone.phone)
        return "Done!"

    def delete_phone(self, phone):
        for p in phone.phone:
            if p in self.Phones.phone:
                self.Phones.phone.remove(p)
        return "Done!"

    def change_birthday(self, birthday):
        self.Birthday = birthday
        return "Done!"

    def delete_birthday(self):
        self.Birthday.birthday = []
        return "Done!"

    def change_email(self, email):
        self.Emails = email
        return "Done!"

    def delete_email(self, email):
        for e in email.email:
            if e in self.Emails.email:
                self.Emails.email.remove(e)
        return "Done!"

    def change_address(self, address):
        self.Address = address
        return "Done!"

    def delete_address(self):
        self.Address.address = []
        return "Done!"

    def days_to_birthday(self):
        if not self.Birthday.birthday:
            return "The birthday date is unknown."

        current_datetime = datetime.now()
        birthday = datetime.strptime(self.Birthday.birthday[0], '%d/%m/%Y')
        if (
            current_datetime.month > birthday.month
            or (current_datetime.month == birthday.month and current_datetime.day >= birthday.day)
        ):
            next_birthday = datetime(
                year=current_datetime.year + 1, month=birthday.month, day=birthday.day)
            return f"In {(next_birthday - current_datetime).days} days"
        else:
            next_birthday = datetime(
                year=current_datetime.year, month=birthday.month, day=birthday.day)
            return f"Birthday in {(next_birthday - current_datetime).days} days"

    def __str__(self):
        return f"{self.Name.name} | {' '.join(self.Phones.phone)} | {self.Birthday.birthday[0] if self.Birthday.birthday else ''} | {' '.join(self.Emails.email)} | {' '.join(self.Address.address)}"


class Field:
    def __init__(self, data):
        if isinstance(data, str):  # Check if data is a string
            data = data.split()
        # Update the attributes for individual fields
        self.name = data[0].capitalize() if data else ''
        self.phone = [phone for phone in data if len(
            phone) >= 10 and len(phone) <= 12 and phone.isdigit()]
        self.birthday = [date for date in data if re.match(
            r'\d{2}/\d{2}/\d{4}', date)]
        self.email = [email for email in data if re.match(
            r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b', email)]
        self.address = [address for address in data if address.startswith('/')]


class Phone(Field):
    pass


class Birthday(Field):
    pass


class Email(Field):
    pass


class Name(Field):
    pass


class Address(Field):
    pass


class UserInterface(ABC):
    @abstractmethod
    def display_contacts(self, contacts):
        pass

    @abstractmethod
    def display_commands(self, commands):
        pass


def input_error(func):
    def inner():
        flag = True
        while flag:
            try:
                result = func()
                flag = False
            except IndexError:
                print('Enter the name and numbers separated by a space.')
            except ValueError:
                print('I have no idea how you did it, try again.')
            except KeyError:
                print("The contact is missing.")
        return result
    return inner


def validate_field(info, pattern, error_msg):
    field_data = [field for field in info if re.match(pattern, field)]
    if len(field_data) != 1:
        print(error_msg)
    return field_data[0] if field_data else None


def add_contact(CONTACTS):
    print(tutorial)
    contact_info = get_valid_input(
        "Enter contact's name, phone number(s), email(s), birthday (dd/mm/yyyy), and address: ")

    data = contact_info.split(maxsplit=4)
    if len(data) < 5:
        print("Invalid information provided.")
        return

    name, phone_data, email_data, birthday_data, address_data = data

    phones = re.findall(r'\b\d{10,12}\b', phone_data)
    emails = re.findall(
        r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b', email_data)
    birthday = re.findall(r'\b\d{2}/\d{2}/\d{4}\b', birthday_data)
    address = re.findall(r'\/(?:[^\/]*\/)*[^\/]+\/\d+\b', address_data)

    if not name or not phones or not emails or not birthday or not address:
        print("Invalid information provided.")
        return

    if name in CONTACTS.data:
        CONTACTS.data[name].add_phone(Phone(phones))
    else:
        CONTACTS.add_record(Record(Name(name), Phone(phones),
                                   Birthday(birthday), Email(emails), Address(address)))


def show_contact_phones(CONTACTS):
    command = input('Enter the name of the contact: ').capitalize()
    if command in CONTACTS.data:
        print(
            f"Contact's phones: {', '.join(CONTACTS.data[command].Phones.phone)}")
    else:
        print("Contact not found!")


def search_contacts(CONTACTS):
    command = input('Enter any piece of information: ')
    if result := CONTACTS.find(command):
        for contact_info in result:
            print(contact_info)
    else:
        print('No matches')


def show_days_to_birthday(CONTACTS):
    command = input('Enter the name of the contact: ').capitalize()
    print(CONTACTS.days_to_birthday(command))


def show_contacts_in_days(CONTACTS):
    command = int(input('Enter the number of days: '))
    if contacts_in_days := CONTACTS.contacts_in_days(command):
        print("The following contacts have birthdays within", command, "days:")
        for contact in contacts_in_days:
            print("-", contact)
    else:
        print("No contacts found with birthdays within", command, "days.")


def change_contact_data(CONTACTS):
    print("Choose the action:")
    print("1. Add phone")
    print("2. Delete phone")
    print("3. Change birthday")
    print("4. Delete birthday")
    print("5. Change email")
    print("6. Delete email")
    print("7. Change address")
    print("8. Delete address")
    print("9. Go back")
    action = input("Enter the number of the action: ")
    command = input('Enter the name of the contact: ').capitalize()
    if command in CONTACTS.data:
        if action == '1':
            CONTACTS.data[command].add_phone(
                Phone(input("Enter the phone number(s) separated by space: ")))
        elif action == '2':
            CONTACTS.data[command].delete_phone(
                Phone(input("Enter the phone number(s) separated by space: ")))
        elif action == '3':
            CONTACTS.data[command].change_birthday(
                Birthday(input("Enter the birthday (dd/mm/yyyy): ")))
        elif action == '4':
            CONTACTS.data[command].delete_birthday()
        elif action == '5':
            CONTACTS.data[command].change_email(
                Email(input("Enter the email(s) separated by space: ")))
        elif action == '6':
            CONTACTS.data[command].delete_email(
                Email(input("Enter the email(s) separated by space: ")))
        elif action == '7':
            CONTACTS.data[command].change_address(
                Address(input("Enter the address: ")))
        elif action == '8':
            CONTACTS.data[command].delete_address()
        elif action != '9':
            print("Invalid action.")
    else:
        print("Contact not found!")


def delete_contact_data(CONTACTS):
    print("Choose the action:")
    print("1. Delete phone")
    print("2. Delete email")
    print("3. Delete birthday")
    print("4. Delete address")
    print("5. Delete contact")
    print("6. Go back")
    action = input("Enter the number of the action: ")
    command = input('Enter the name of the contact: ').capitalize()
    if command in CONTACTS.data:
        if action == '1':
            CONTACTS.data[command].delete_phone(
                Phone(input("Enter the phone number(s) separated by space: ")))
        elif action == '2':
            CONTACTS.data[command].delete_email(
                Email(input("Enter the email(s) separated by space: ")))
        elif action == '3':
            CONTACTS.data[command].delete_birthday()
        elif action == '4':
            CONTACTS.data[command].delete_address()
        elif action == '5':
            CONTACTS.delete_record(command)
        elif action != '6':
            print("Invalid action.")
    else:
        print("Contact not found!")


def save_address_book(CONTACTS):
    CONTACTS.save_to_file("address_book.txt")
    print("Address book data saved.")


def load_address_book(CONTACTS):
    CONTACTS.load_from_file("address_book.txt")
    print("Address book data loaded.")


class ConsoleUI(UserInterface):
    def display_contacts(self, contacts):
        table = PrettyTable(['Name', 'Phone', 'Birthday', 'Email', 'Address'])
        for contact in contacts:
            table.add_row([contact.Name.name,
                           ", ".join(contact.Phones.phone),
                           contact.Birthday.birthday[0] if contact.Birthday.birthday else "",
                           ", ".join(contact.Emails.email),
                           contact.Address.address[0] if contact.Address.address else ""])
        print(table)

    def display_commands(self, commands):
        table = PrettyTable(['Command', 'Instruction'])
        table.add_rows(commands)
        table.align["Instruction"] = "l"
        print(table)


def save_address_book_to_file(filename, contacts):
    with open(filename, "w") as file:
        for record in contacts.data.values():
            formatted_record = contacts._format_record_to_txt(record)
            file.write(formatted_record + "\n")
    print("Address book data saved to txt file.")


def main():
    try:
        with open("address_book.pkl", "rb") as fh:
            CONTACTS = pickle.load(fh)
    except (EOFError, pickle.UnpicklingError):
        print("Error loading data. Creating a new AddressBook.")
        CONTACTS = AddressBook()
    except FileNotFoundError:
        CONTACTS = AddressBook()

    console_interface = ConsoleUI()

    commands = [
        ["1", "Add a contact to the address book"],
        ["2", "Shows phone numbers of a particular contact"],
        ["3", "Search for matches among existing contacts"],
        ["4", "Calculates the number of days until the contact's next birthday"],
        ["5", "Displays the names of contacts whose birthday is in the specified number of days"],
        ["6", "Change any contact's data"],
        ["7", "Delete any contact's data"],
        ["8", "Show you the full list of contacts in the address book"],
        ["9", "Exit the address book"],
        ["10", "Load address book data from a file"],
        ["11", "Save address book data to a file"],
    ]

    while True:
        console_interface.display_commands(commands)
        command = input("Enter the command number: ")

        if command == "1":
            add_contact(CONTACTS)
        elif command == "2":
            show_contact_phones(CONTACTS)
        elif command == "3":
            search_contacts(CONTACTS)
        elif command == "4":
            show_days_to_birthday(CONTACTS)
        elif command == "5":
            show_contacts_in_days(CONTACTS)
        elif command == "6":
            change_contact_data(CONTACTS)
        elif command == "7":
            delete_contact_data(CONTACTS)
        elif command == "8":
            console_interface.display_contacts(CONTACTS.show_all())
        elif command == "9":
            save_address_book_to_file("address_book.txt", CONTACTS)
            break
        elif command == "10":
            CONTACTS.load_address_book_from_txt("address_book.txt")
        elif command == "11":
            save_address_book_to_file("address_book.txt", CONTACTS)
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
