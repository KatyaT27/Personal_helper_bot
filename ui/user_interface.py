from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def show_menu(self):
        pass

    @abstractmethod
    def display_address_book(self, contacts):
        pass

    @abstractmethod
    def display_notes(self, notes):
        pass
