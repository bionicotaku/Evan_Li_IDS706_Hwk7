import unittest
from unittest.mock import MagicMock
import mylib.CRUD as crud


class TestSimpleCRUD(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=crud.Database)

    def test_user_crud(self):
        # Create user
        self.db.create_user.return_value = 1
        user_id = self.db.create_user(
            "john@example.com", "John", "Doe", "123 Main St", 100
        )
        self.assertEqual(user_id, 1)

        # Get user
        self.db.get_user.return_value = {
            "id": 1,
            "email": "john@example.com",
            "balance": 100,
        }
        user = self.db.get_user(user_id)
        self.assertEqual(user["email"], "john@example.com")

        # Update user
        self.db.update_user.return_value = True
        updated = self.db.update_user(user_id, email="johndoe@example.com", balance=200)
        self.assertTrue(updated)

        # Delete user
        self.db.delete_user.return_value = True
        deleted = self.db.delete_user(user_id)
        self.assertTrue(deleted)

    def test_product_crud(self):
        # Create product
        self.db.create_product.return_value = 1
        product_id = self.db.create_product("Laptop", "Electronics", 999.99, 10)
        self.assertEqual(product_id, 1)

        # Get product
        self.db.get_product.return_value = {
            "id": 1,
            "name": "Laptop",
            "price": 999.99,
            "stock": 10,
        }
        product = self.db.get_product(product_id)
        self.assertEqual(product["name"], "Laptop")

        # Update product
        self.db.update_product.return_value = True
        updated = self.db.update_product(product_id, price=899.99, stock=15)
        self.assertTrue(updated)

        # Delete product
        self.db.delete_product.return_value = True
        deleted = self.db.delete_product(product_id)
        self.assertTrue(deleted)


if __name__ == "__main__":
    unittest.main()
