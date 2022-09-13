""" BookInventory test """

import unittest
from .. import BookInventory


class TestBookInventory(unittest.TestCase):

    def test_get_all_books(self):
        book_inventory = BookInventory()
        books = book_inventory.get_all_books()
        self.assertIsInstance(books, list)

    def test_get_book_by_string_id(self):
        book_inventory = BookInventory()
        book = book_inventory.get_book("1")
        self.assertIsNotNone(book)
        self.assertTrue(isinstance(book['id'], int))
        self.assertTrue(isinstance(book['author'], str))

    def test_get_book_by_numeric_id(self):
        book_inventory = BookInventory()
        book = book_inventory.get_book(1)
        self.assertIsNotNone(book)
        self.assertTrue(isinstance(book['id'], int))
        self.assertTrue(isinstance(book['author'], str))

    def test_add_book(self):
        title = "The Equinor Book"
        author = "Anders Opedal"
        abstract = "The essentials of being an Equinor employee"
        book_inventory = BookInventory()
        book = book_inventory.add_book(title, author, abstract)
        self.assertIsNotNone(book)
        self.assertEqual(book['title'], title)
        self.assertEqual(book['author'], author)

    def test_update_book_by_numeric_id(self):
        title = "The Equionor Book"
        author = "Anders Opedal"
        abstract = "The essentials of being an Equinor employee"
        book_id = 1
        book_inventory = BookInventory()
        book = book_inventory.update_book(book_id, title, author, abstract)
        self.assertIsNotNone(book)
        self.assertEqual(book['title'], title)
        self.assertEqual(book['author'], author)
        self.assertEqual(book['id'], book_id)

    def test_update_book_by_string_id(self):
        title = "The Equinor Book"
        author = "Anders Opedal"
        abstract = "The essentials of being an Equinor employee"        
        book_id = 1
        book_inventory = BookInventory()
        book = book_inventory.update_book(str(book_id), title, author, abstract)
        self.assertIsNotNone(book)
        self.assertEqual(book['title'], title)
        self.assertEqual(book['author'], author)
        self.assertEqual(book['id'], book_id)

    def test_delete_book_by_string_id(self):
        book_id = 1
        book_inventory = BookInventory()
        self.assertTrue(book_inventory.has_book(book_id))
        book_inventory.delete_book(book_id)
        self.assertTrue(not book_inventory.has_book(book_id))

    def test_inventory_count(self):
        book_inventory = BookInventory()
        books = book_inventory.get_all_books()
        self.assertEqual(len(books), book_inventory.count())
        book_inventory.delete_book(1)
        books = book_inventory.get_all_books()
        self.assertEqual(book_inventory.count(), book_inventory.count())

if __name__ == '__main__':
    unittest.main()
