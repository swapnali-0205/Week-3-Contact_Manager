import json
import csv
import os
import re
from datetime import datetime

FILE_NAME = "contacts.json"
BACKUP_FILE = "contacts_backup.json"


# -------------------- VALIDATION HELPERS --------------------

def clean_name(name):
    return name.strip().title()


def validate_name(name):
    return bool(re.fullmatch(r"[A-Za-z ]{2,}", name))


def validate_phone(phone):
    return bool(re.fullmatch(r"\+?\d{7,15}", phone))


def validate_email(email):
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))


# -------------------- FILE OPERATIONS --------------------

def load_from_file():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {}


def save_to_file(contacts):
    with open(FILE_NAME, "w") as f:
        json.dump(contacts, f, indent=4)
    create_backup(contacts)


def create_backup(contacts):
    with open(BACKUP_FILE, "w") as f:
        json.dump(contacts, f, indent=4)


# -------------------- CRUD FUNCTIONS --------------------

def add_contact(contacts):
    name = clean_name(input("Enter name: "))
    if not validate_name(name):
        print("❌ Invalid name.")
        return

    if name in contacts:
        print("❌ Contact already exists.")
        return

    phone = input("Enter phone number: ")
    if not validate_phone(phone):
        print("❌ Invalid phone number.")
        return

    email = input("Enter email: ")
    if not validate_email(email):
        print("❌ Invalid email.")
        return

    address = input("Enter address: ").strip()
    group = input("Enter group (Family, Work, Friends): ").strip().title()

    contacts[name] = {
        "phone": phone,
        "email": email,
        "address": address,
        "group": group,
        "created": datetime.now().isoformat()
    }

    save_to_file(contacts)
    print("✅ Contact added successfully!")


def search_contact(contacts):
    query = input("Search by name or phone: ").strip().lower()
    found = False

    for name, data in contacts.items():
        if query in name.lower() or query in data["phone"]:
            display_contact(name, data)
            found = True

    if not found:
        print("❌ No matching contacts found.")


def update_contact(contacts):
    name = clean_name(input("Enter contact name to update: "))

    if name not in contacts:
        print("❌ Contact not found.")
        return

    phone = input("New phone (leave blank to keep current): ")
    email = input("New email (leave blank to keep current): ")
    address = input("New address (leave blank to keep current): ")
    group = input("New group (leave blank to keep current): ")

    if phone:
        if not validate_phone(phone):
            print("❌ Invalid phone number.")
            return
        contacts[name]["phone"] = phone

    if email:
        if not validate_email(email):
            print("❌ Invalid email.")
            return
        contacts[name]["email"] = email

    if address:
        contacts[name]["address"] = address

    if group:
        contacts[name]["group"] = group.title()

    save_to_file(contacts)
    print("✅ Contact updated successfully!")


def delete_contact(contacts):
    name = clean_name(input("Enter contact name to delete: "))

    if name not in contacts:
        print("❌ Contact not found.")
        return

    confirm = input(f"Are you sure you want to delete {name}? (y/n): ").lower()
    if confirm == "y":
        del contacts[name]
        save_to_file(contacts)
        print("✅ Contact deleted.")
    else:
        print("❌ Deletion canceled.")


def display_all(contacts):
    if not contacts:
        print("📭 No contacts available.")
        return

    for name, data in sorted(contacts.items()):
        display_contact(name, data)


def display_contact(name, data):
    print("-" * 40)
    print(f"Name    : {name}")
    print(f"Phone   : {data['phone']}")
    print(f"Email   : {data['email']}")
    print(f"Address : {data['address']}")
    print(f"Group   : {data['group']}")
    print("-" * 40)


# -------------------- ADVANCED FEATURES --------------------

def export_to_csv(contacts):
    with open("contacts.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email", "Address", "Group"])
        for name, data in contacts.items():
            writer.writerow([name, data["phone"], data["email"], data["address"], data["group"]])
    print("📤 Contacts exported to contacts.csv")


def show_statistics(contacts):
    print(f"📊 Total contacts: {len(contacts)}")
    groups = {}
    for data in contacts.values():
        group = data["group"]
        groups[group] = groups.get(group, 0) + 1

    for group, count in groups.items():
        print(f"  {group}: {count}")


# -------------------- MENU SYSTEM --------------------

def main_menu():
    print("""
📇 CONTACT MANAGEMENT SYSTEM
1. Add Contact
2. Search Contact
3. Update Contact
4. Delete Contact
5. Display All Contacts
6. Export to CSV
7. Statistics
0. Exit
""")


def main():
    contacts = load_from_file()

    while True:
        main_menu()
        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                add_contact(contacts)
            elif choice == "2":
                search_contact(contacts)
            elif choice == "3":
                update_contact(contacts)
            elif choice == "4":
                delete_contact(contacts)
            elif choice == "5":
                display_all(contacts)
            elif choice == "6":
                export_to_csv(contacts)
            elif choice == "7":
                show_statistics(contacts)
            elif choice == "0":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice.")
        except Exception as e:
            print(f"⚠️ Error: {e}")


if __name__ == "__main__":
    main()
