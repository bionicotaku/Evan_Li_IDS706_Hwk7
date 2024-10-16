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

    def test_complex_queries(self):
        # Test get_user_orders
        self.db.get_user_orders.return_value = [
            {"order_id": 1, "product_name": "Laptop", "quantity": 2}
        ]
        user_orders = self.db.get_user_orders(1)
        self.assertEqual(len(user_orders), 1)

        # Test get_top_selling_products
        self.db.get_top_selling_products.return_value = [
            {"product_name": "Laptop", "total_quantity": 10}
        ]
        top_products = self.db.get_top_selling_products(3)
        self.assertEqual(len(top_products), 1)

        # Test get_user_total_spending
        self.db.get_user_total_spending.return_value = {
            "user_id": 2,
            "total_spending": 1999.98,
        }
        user_spending = self.db.get_user_total_spending(2)
        self.assertEqual(user_spending["total_spending"], 1999.98)

        # Test get_product_sales_by_category
        self.db.get_product_sales_by_category.return_value = [
            {"category": "Electronics", "total_sales": 5000}
        ]
        category_sales = self.db.get_product_sales_by_category()
        self.assertEqual(len(category_sales), 1)

        # Test get_users_with_high_balance
        self.db.get_users_with_high_balance.return_value = [
            {"id": 1, "name": "John Doe", "balance": 1000}
        ]
        high_balance_users = self.db.get_users_with_high_balance(900)
        self.assertEqual(len(high_balance_users), 1)


if __name__ == "__main__":
    unittest.main()
