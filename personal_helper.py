import logging
from ui.console_ui import ConsoleUI


def main():
    # Configure logging settings
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=logging.INFO,
        filename="personal_helper.log",
        filemode="a",
    )

    # Log the start of the Personal Helper Bot application
    logging.info("Started Personal Helper Bot application.")

    # Create an instance of the ConsoleUI class
    ui = ConsoleUI()

    # Show the menu and interact with the user until the user chooses to exit
    while ui.show_menu():
        pass

    # Log that the Personal Helper Bot application is exiting
    logging.info("Exiting Personal Helper Bot application.")


if __name__ == "__main__":
    main()
