""" Book inventory class """
class BookInventory:

    def __init__(self):
        self.books = {}
        self.add_book('1984', 'George Orwell', 'A dystopian social science fiction novel')
        self.add_book('War and Peace', 'Leo Tolstoy', 'A literary work mixed with chapters on history and philosophy')
        self.add_book('Robinson Crusoe', 'Daniel Defoe', 'An autobiography of castaway spending years on remote island')

    def get_all_books(self):
        return list(self.books.values())

    def get_book(self, book_id):
        return self.books.get(str(book_id))

    def add_book(self, title, author, abstract):
        book_id = self._find_first_available_id()
        return self._add_book(book_id, title, author, abstract)

    def update_book(self, book_id, title, author, abstract):
        return self._add_book(book_id, title, author, abstract)

    def has_book(self, book_id):
        return str(book_id) in self.books

    def delete_book(self, book_id):
        self.books.pop(str(book_id))

    def count(self):
        return len(self.books)

    def search(self, keyword):
        results = []
        for book in self.books.values():
            if book['title'].find(keyword) >= 0 \
                or book['author'].find(keyword) >= 0 \
                or book['abstract'].find(keyword) >= 0 :
                results.append(book)
        return results

    def _add_book(self, book_id, title, author, abstract):
        book = {'id': int(book_id), 'title': title, 'author': author, 'abstract': abstract}
        self.books[str(book_id)] = book
        return book

    def _find_first_available_id(self):
        if len(self.books) == 0:
            return 0
        max_id = max(map(int, self.books.keys()))
        for key in range(max_id):
            if str(key) not in self.books:
                return key
        return max_id + 1
