"""
CLI for the Address Book.

Commands:
add <name> <phone>                    - Add a contact (or add another phone to existing one).
                                        Phone must be exactly 10 digits.
change <name> <old_phone> <new_phone> - Replace an existing phone with a new one (10 digits).
phone <name>                          - Show all phones for a contact.
all                                   - Show all contacts.
add-birthday <name> <DD.MM.YYYY>      - Add a birthday to a contact.
show-birthday <name>                  - Show a contact's birthday.
birthdays                             - Show upcoming birthdays within 7 days (Sat/Sun -> Monday).
delete <name>                         - Delete a contact.
help                                  - Show help.
exit | close | goodbye                - Exit program.
"""

from address_book import (
    AddressBook,
    add_contact,
    change_contact,
    show_phones,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)

EXIT_COMMANDS = {"exit", "close", "goodbye", "quit"}


def parse_input(line: str):
    """
    Splits raw line into (command, args_list).
    """
    line = line.strip()
    if not line:
        return "", []
    parts = line.split()
    return parts[0].lower(), parts[1:]


def print_help():
    print(
        "Available commands:\n"
        "  add <name> <phone>                    - Add a contact or another phone (10 digits).\n"
        "  change <name> <old_phone> <new_phone> - Replace a phone (10 digits).\n"
        "  phone <name>                          - Show all phones for a contact.\n"
        "  all                                   - Show all contacts.\n"
        "  add-birthday <name> <DD.MM.YYYY>      - Add a birthday to a contact.\n"
        "  show-birthday <name>                  - Show a contact's birthday.\n"
        "  birthdays                             - Show upcoming birthdays (7 days; weekend -> Monday).\n"
        "  delete <name>                         - Delete a contact.\n"
        "  help                                  - Show this help.\n"
        "  exit | close | goodbye                - Exit the program.\n"
    )


def main():
    book = AddressBook()
    print("Welcome to Address Book! Type 'help' to see available commands.")
    print_help()

    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        cmd, args = parse_input(line)
        if not cmd:
            continue

        if cmd in EXIT_COMMANDS:
            print("Goodbye!")
            break

        if cmd == "help":
            print_help()

        elif cmd == "add":
            if len(args) < 2:
                print("Error: Usage -> add <name> <phone>")
                continue
            # name can be multi-word; last arg is phone
            name = " ".join(args[:-1])
            phone = args[-1]
            print(add_contact([name, phone], book))

        elif cmd == "change":
            if len(args) < 3:
                print("Error: Usage -> change <name> <old_phone> <new_phone>")
                continue
            # name can be multi-word; last two are phones
            name = " ".join(args[:-2])
            old_phone = args[-2]
            new_phone = args[-1]
            print(change_contact([name, old_phone, new_phone], book))

        elif cmd == "phone":
            if not args:
                print("Error: Usage -> phone <name>")
                continue
            name = " ".join(args)
            print(show_phones([name], book))

        elif cmd == "all":
            print(show_all(book))

        elif cmd == "add-birthday":
            if len(args) < 2:
                print("Error: Usage -> add-birthday <name> <DD.MM.YYYY>")
                continue
            name = " ".join(args[:-1])
            date_str = args[-1]
            print(add_birthday([name, date_str], book))

        elif cmd == "show-birthday":
            if not args:
                print("Error: Usage -> show-birthday <name>")
                continue
            name = " ".join(args)
            print(show_birthday([name], book))

        elif cmd == "birthdays":
            print(birthdays([], book))

        elif cmd == "delete":
            if not args:
                print("Error: Usage -> delete <name>")
                continue
            name = " ".join(args)
            if book.find(name):
                book.delete(name)
                print("Contact deleted.")
            else:
                print("Error: Contact not found.")

        else:
            print("Unknown command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()