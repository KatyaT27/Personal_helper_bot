from prettytable import PrettyTable
from address_book.address_book import main as address_book_main
from notes.notes import main as notes_main
from sort.sort import main as sort_main


class ConsoleUI:
    def show_menu(self):
        menu_data = [
            ["1", "Go to Address Book"],
            ["2", "Go to Notes"],
            ["3", "Go to Sorter"],
            ["4", "Exit the program"]
        ]

        menu_table = PrettyTable(field_names=["Command", "Instruction"])
        for row in menu_data:
            menu_table.add_row(row)

        print(f"\nPersonal Helper Menu:\n{menu_table}")

        while True:
            try:
                command = int(input("Enter command to Personal Helper: "))
                if command == 1:
                    print("You went to Address Book")
                    address_book_main()
                elif command == 2:
                    print("You went to Notes")
                    notes_main()
                elif command == 3:
                    print("You went to Sorter")
                    sort_main()
                elif command == 4:
                    print("Goodbye!")
                    return False  # Exit the loop and the program
                else:
                    print("Invalid command. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    ui = ConsoleUI()
    while ui.show_menu():
        pass
