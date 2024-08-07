from datetime import datetime, timedelta

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me correct arguments, please."
        except KeyError:
            return "Give an existing name, please."
        except IndexError:
            return "Not enough arguments provided."
    return inner

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    contacts[name] = contacts.get(name, []) + [phone]
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) != 3:
        raise ValueError
    name, old_phone, new_phone = args
    if name in contacts:
        if old_phone in contacts[name]:
            contacts[name].remove(old_phone)
            contacts[name].append(new_phone)
            return "Contact changed."
        else:
            raise KeyError
    else:
        raise KeyError

@input_error
def show_phone(contacts):
    if not contacts:
        return "No contacts available."
    return "\n".join([f"{name}: {', '.join(phones)}" for name, phones in contacts.items()])

@input_error
def contact_search(args, contacts):
    if len(args) != 1:
        raise ValueError
    name = args[0]
    if name in contacts:
        return f"{name}: {', '.join(contacts[name])}"
    else:
        return "Contact not found."

@input_error
def add_birthday(args, contacts, birthdays):
    if len(args) != 2:
        raise ValueError
    name, birthday = args
    try:
        date = datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."
    if name in contacts:
        birthdays[name] = date
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, birthdays):
    if len(args) != 1:
        raise ValueError
    name = args[0]
    if name in birthdays:
        return f"{name}'s birthday is on {birthdays[name].strftime('%Y-%m-%d')}"
    else:
        return "Birthday not found."

def birthdays_within_week(birthdays):
    upcoming_birthdays = []
    today = datetime.now().date()
    week_later = today + timedelta(days=7)
    for name, date in birthdays.items():
        if today <= date.date() <= week_later:
            upcoming_birthdays.append(f"{name}: {date.strftime('%Y-%m-%d')}")
    if not upcoming_birthdays:
        return "No upcoming birthdays within a week."
    return "\n".join(upcoming_birthdays)

def main():
    contacts = {}
    birthdays = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "all":
            print(show_phone(contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(contact_search(args, contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts, birthdays))
        elif command == "show-birthday":
            print(show_birthday(args, birthdays))
        elif command == "birthdays":
            print(birthdays_within_week(birthdays))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
