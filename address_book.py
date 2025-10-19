from collections import UserDict
from datetime import datetime, timedelta

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, KeyError) as e:
            return f"Error: {str(e)}"
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        s = str(value)
        if not s.isdigit() or len(s) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(s)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_str):
        phone = Phone(phone_str)
        self.phones.append(phone)

    def remove_phone(self, phone_str):
        phone = self.find_phone(phone_str)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError(f"Phone number {phone_str} not found.")

    def edit_phone(self, old_phone_str, new_phone_str):
        phone = self.find_phone(old_phone_str)
        if not phone:
            raise ValueError(f"Phone number {old_phone_str} not found.")
        new_phone = Phone(new_phone_str)
        self.remove_phone(old_phone_str)
        self.phones.append(new_phone)

    def change_phone(self, old, new):
        for i, p in enumerate(self.phones):
            if p.value == old:
                self.phones[i] = Phone(new)
                return True
        return False

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone_str):
        for phone in self.phones:
            if phone.value == phone_str:
                return phone
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        bday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {bday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                delta = (bday - today).days
                if 0 <= delta <= 7:
                    if bday.weekday() == 5:  # Saturday
                        bday += timedelta(days=2)
                    elif bday.weekday() == 6:  # Sunday
                        bday += timedelta(days=1)
                    upcoming.append({
                        "name": record.name.value,
                        "birthday": bday.strftime("%d.%m.%Y")
                    })
        return upcoming

    def __str__(self):
        if not self.data:
            return "AddressBook: <empty>"
        return "\n".join(str(record) for record in self.data.values())


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record and record.change_phone(old_phone, new_phone):
        return "Phone number updated."
    return "Contact or phone not found."

@input_error
def show_phones(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return ", ".join(p.value for p in record.phones) if record.phones else "No phones saved."
    return "Contact not found."

@input_error
def show_all(book):
    return str(book)

@input_error
def add_birthday(args, book):
    name, bday = args
    record = book.find(name)
    if record:
        record.add_birthday(bday)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return "Birthday not found."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join([f"{item['name']}: {item['birthday']}" for item in upcoming])
