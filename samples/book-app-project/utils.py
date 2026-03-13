from typing import List
from books import Book


def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print("Invalid choice. Please enter a number between 1 and 5.")


def get_book_details() -> tuple[str, str, int]:
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print("Title cannot be empty. Please try again.")
    
    while True:
        author = input("Enter author: ").strip()
        if author:
            break
        print("Author cannot be empty. Please try again.")

    while True:
        year_input = input("Enter publication year: ").strip()
        try:
            year = int(year_input)
            if year >= 0:
                break
            print("Please enter a valid year (must be non-negative).")
        except ValueError:
            print("Invalid input. Please enter a number for the year.")

    return title, author, year


def print_books(books: List[Book]) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    try:
        for index, book in enumerate(books, start=1):
            status = "✅ Read" if book.read else "📖 Unread"
            print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
    except AttributeError as e:
        print(f"Error displaying books: Missing book attribute - {e}")
    except Exception as e:
        print(f"Unexpected error while displaying books: {e}")
