import abc
from prettytable import PrettyTable
import os
import shutil
import sys
import zipfile
import tarfile
import gzip


# Define an abstract base class for user interfaces
class UserInterface(abc.ABC):
    @abc.abstractmethod
    def show_menu(self, table):
        pass

    @abc.abstractmethod
    def get_command(self):
        pass

    @abc.abstractmethod
    def show_message(self, message):
        pass


# Implement the concrete class for the console user interface


class ConsoleUserInterface(UserInterface):
    def show_menu(self, table):
        print("\nSorter Menu:")
        print(table)

    def get_command(self):
        return input("Enter the command number: ")

    def show_message(self, message):
        print(message)


def normalize(name):
    translit_dict = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "є": "ye",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "і": "i",
        "ї": "yi",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ь": "",
        "ю": "yu",
        "я": "ya",
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Є": "YE",
        "Ж": "ZH",
        "З": "Z",
        "И": "I",
        "І": "I",
        "Ї": "YI",
        "Й": "Y",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "KH",
        "Ц": "TS",
        "Ч": "CH",
        "Ш": "SH",
        "Щ": "SHCH",
        "Ь": "",
        "Ю": "YU",
        "Я": "YA",
    }
    normalized_name = ""
    for char in name:
        if char.isalnum():
            if char.lower() in translit_dict:
                normalized_name += translit_dict[char.lower()]
            else:
                normalized_name += char
        else:
            normalized_name += "_"
    return normalized_name


def sort_files(folder_path):
    image_extensions = (".jpeg", ".png", ".jpg", ".svg")
    video_extensions = (".avi", ".mp4", ".mov", ".mkv")
    document_extensions = (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx")
    music_extensions = (".mp3", ".ogg", ".wav", ".amr")
    archive_extensions = (".zip", ".tar", ".gz")

    for root, dirs, files in os.walk(folder_path, topdown=True):
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            file_name = os.path.splitext(file)[0]
            normalized_name = normalize(file_name)

            if file_extension in archive_extensions:
                extract_path = os.path.join(root, file)
                extract_file(extract_path, folder_path)
                continue

            if file_extension in image_extensions:
                destination_folder = os.path.join(folder_path, "images")
            elif file_extension in video_extensions:
                destination_folder = os.path.join(folder_path, "video")
            elif file_extension in document_extensions:
                destination_folder = os.path.join(folder_path, "documents")
            elif file_extension in music_extensions:
                destination_folder = os.path.join(folder_path, "audio")
            else:
                destination_folder = os.path.join(folder_path, "unknown")

            os.makedirs(destination_folder, exist_ok=True)

            new_file_path = os.path.join(
                destination_folder, normalized_name + file_extension
            )

            shutil.move(os.path.join(root, file), new_file_path)

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def extract_file(file_path, destination_folder):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".zip":
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(destination_folder)
    elif file_extension == ".tar":
        with tarfile.open(file_path, "r") as tar_ref:
            tar_ref.extractall(destination_folder)
    elif file_extension == ".gz":
        with gzip.open(file_path, "rb") as gz_ref:
            extract_path = os.path.join(
                destination_folder, os.path.basename(file_path[:-3])
            )
            with open(extract_path, "wb") as extract_file:
                extract_file.write(gz_ref.read())

    os.remove(file_path)


def main():
    table = PrettyTable(["Command", "Instruction"])
    table.add_rows(
        [
            ["1", "Sort any folder"],
            ["2", "Exit the Sorter"],
        ]
    )

    # Create the console user interface object
    ui = ConsoleUserInterface()

    while True:
        ui.show_menu(table)
        command = ui.get_command()

        if command == "1":
            folder_name = input("Enter the folder path to sort: ")
            folder_path = os.path.abspath(folder_name)

            if not os.path.isdir(folder_path):
                ui.show_message("Invalid folder path.")
                sys.exit(1)

            sort_files(folder_path)
            ui.show_message("File sorting completed successfully.")

        elif command == "2":
            break

        else:
            ui.show_message("Invalid command.")


if __name__ == "__main__":
    main()
