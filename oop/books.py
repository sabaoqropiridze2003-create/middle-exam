import sys


class Book:

    def __init__(self, title, author, year):
        self.__title = title
        self.__author = author
        self.__year = year

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_year(self):
        return self.__year

    def get_details(self):
        return f"[physical Book] Title: {self.__title} | Author: {self.__author} | Year: {self.__year}"

    def to_file_format(self):
        return f"BOOK,{self.__title},{self.__author},{self.__year}"


class EBook(Book):

    def __init__(self, title, author, year, file_size_mb):
        super().__init__(title, author, year)
        self.__file_size_mb = file_size_mb

    def get_file_size_mb(self):
        return self.__file_size_mb

    def get_details(self):
        return (f"[E-Book] Title: {self.get_title()} | Author: {self.get_author()} | "
                f"Year: {self.get_year()} | Size: {self.__file_size_mb} MB")

    def to_file_format(self):
        return f"EBOOK,{self.get_title()},{self.get_author()},{self.get_year()},{self.__file_size_mb}"


class BookManager:

    def __init__(self, file_name="oop/books.txt"):
        self.file_name = file_name
        self.books = []
        self.load_from_file()

    def add_book(self, book):
        self.books.append(book)
        self.save_to_file()
        print("\n✅ Book added successfully!")

    def display_all_books(self):
        if not self.books:
            print("\nThe book list is empty.")
            return

        print("\n--- Book List ---")
        for idx, book in enumerate(self.books, start=1):
            print(f"{idx}. {book.get_details()}")

    def search_book_by_title(self, search_title):
        found_books = []
        for book in self.books:
            if search_title.lower() in book.get_title().lower():
                found_books.append(book)

        if found_books:
            print(f"\nFound {len(found_books)} book(s):")
            for book in found_books:
                print(f" - {book.get_details()}")
        else:
            print(f"\nNo book found with title '{search_title}'.")

    def delete_book_by_title(self, title_to_delete):
        initial_count = len(self.books)

        self.books = [book for book in self.books if book.get_title(
        ).lower() != title_to_delete.lower()]

        if len(self.books) < initial_count:
            self.save_to_file()
            print(
                f"\nBook with title '{title_to_delete}' deleted successfully!")
        else:
            print(
                f"\nBook with title '{title_to_delete}' not found for deletion.")

    def save_to_file(self):

        try:
            with open(self.file_name, "w") as file:
                for book in self.books:
                    file.write(book.to_file_format() + "\n")
        except Exception as e:
            print(f"\nError saving to file: {e}")

    def load_from_file(self):
        try:
            with open(self.file_name, "r") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(",")
                    if not data or data[0] == "":
                        continue

                    book_type = data[0]
                    if book_type == "BOOK":
                        title, author, year = data[1], data[2], int(data[3])
                        self.books.append(Book(title, author, year))
                    elif book_type == "EBOOK":
                        title, author, year, size = data[1], data[2], int(
                            data[3]), float(data[4])
                        self.books.append(EBook(title, author, year, size))
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"\nError loading from file: {e}")


def input_check(prompt):

    user_input = input(prompt).strip()
    if user_input.lower() == "exit":
        print("\n👋 Program terminated by user (exit). Goodbye!")
        sys.exit()
    return user_input


def get_valid_int(prompt):
    while True:
        val_str = input_check(prompt)
        try:
            return int(val_str)
        except ValueError:
            print("Error! Please enter a valid integer (or 'exit' to quit).")


def get_valid_float(prompt):
    while True:
        val_str = input_check(prompt)
        try:
            val = float(val_str)
            if val <= 0:
                print("File size must be a positive number.")
                continue
            return val
        except ValueError:
            print("Error! Please enter a valid number (or 'exit' to quit).")


def main():
    manager = BookManager()

    while True:
        print("\n==============================")
        print("Book Management System")
        print("(Type 'exit' at any stage to terminate the program)")
        print("==============================")
        print("1. Add new book")
        print("2. View all books")
        print("3. Search book by title")
        print("4. Delete book")
        print("5. Exit")

        choice = input_check("Select an operation (1-5): ")

        if choice == "1":
            print("\n--- Add Book ---")
            title = input_check("Enter title: ")
            while not title:
                print("Title cannot be empty!")
                title = input_check("Enter title: ")

            author = input_check("Enter author: ")
            while not author:
                print("Author cannot be empty!")
                author = input_check("Enter author: ")

            year = get_valid_int("Enter publication year: ")

            print("\nBook Type:")
            print("1. Standard Printed Book")
            print("2. Electronic Book (EBook)")
            type_choice = input_check("Select type (1 or 2): ")

            if type_choice == "2":
                file_size = get_valid_float("Enter file size (MB): ")
                new_book = EBook(title, author, year, file_size)
            else:
                new_book = Book(title, author, year)

            manager.add_book(new_book)

        elif choice == "2":
            manager.display_all_books()

        elif choice == "3":
            search_title = input_check("\nEnter search title: ")
            if search_title:
                manager.search_book_by_title(search_title)
            else:
                print("Search field cannot be empty!")

        elif choice == "4":
            delete_title = input_check(
                "\nEnter the exact title of the book to delete: ")
            if delete_title:
                manager.delete_book_by_title(delete_title)
            else:
                print("Title cannot be empty!")

        elif choice == "5":
            print("\nProgram finished. Thank you!")
            break

        else:
            print("Invalid choice! Please select 1 through 5.")


main()
