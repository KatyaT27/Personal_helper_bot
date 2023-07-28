from prettytable import PrettyTable


class ConsoleUI:
    def show_menu(self):
        print("\nPersonal Helper Menu:")
        print("+---------+--------------------+")
        print("| Command |    Instruction     |")
        print("+---------+--------------------+")
        print("|    1    | Go to Address Book |")
        print("|    2    |    Go to Notes     |")
        print("|    3    |    Go to Sorter    |")
        print("|    4    |  Exit the program  |")
        print("+---------+--------------------+")

        while True:
            try:
                command = int(input("Enter command to Personal Helper: "))
                if command == 1:
                    print("You went to Address Book")
                elif command == 2:
                    print("You went to Notes")
                elif command == 3:
                    print("You went to Sorter")
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
