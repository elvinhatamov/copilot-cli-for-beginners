import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

DATA_FILE = Path("data.json")


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False

    def __post_init__(self):
        if not self.title or not self.author:
            raise ValueError("Title and author cannot be empty")
        if self.year < 0:
            raise ValueError("Year must be non-negative")


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        if not DATA_FILE.exists():
            self.books = []
            return

        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def _find_book_index(self, title: str) -> Optional[int]:
        """Find the index of a book by title (case-insensitive)."""
        title_lower = title.lower()
        for i, book in enumerate(self.books):
            if book.title.lower() == title_lower:
                return i
        return None

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        idx = self._find_book_index(title)
        return self.books[idx] if idx is not None else None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        idx = self._find_book_index(title)
        if idx is not None:
            self.books.pop(idx)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]

    def get_unread_books(self) -> List[Book]:
        """Get all unread books."""
        return [b for b in self.books if not b.read]

    def get_statistics(self) -> dict:
        """Return book collection statistics."""
        return {
            "total": len(self.books),
            "read": sum(1 for b in self.books if b.read),
            "unread": sum(1 for b in self.books if not b.read),
        }

    def search_books(self, query: str) -> List[Book]:
        """Search books by title or author (substring match, case-insensitive)."""
        query_lower = query.lower()
        return [b for b in self.books if query_lower in b.title.lower() or query_lower in b.author.lower()]
