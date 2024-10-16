import mylib.CRUD as crud

# import mylib.setup as setup
from pprint import pprint


def main():
    # setup.setup_database()

    db = crud.Database()

    # User CRUD examples on User table
    user_id = db.create_user("john@example.com", "John", "Doe", "123 Main St", 100)
    user = db.get_user(user_id)
    print(f"Created user with ID: {user_id}, Retrieved user: {user}\n")

    updated = db.update_user(user_id, email="johndoe@example.com", balance=200)
    user = db.get_user(user_id)
    print(f"Update user status: {updated}, Retrieved user: {user}\n")

    deleted = db.delete_user(user_id)
    user = db.get_user(user_id)
    print(f"Delete user status: {deleted}, Retrieved user: {user}\n")

    # Product CRUD examples on Product table
    product_id = db.create_product("Laptop", "Electronics", 999.99, 10)
    product = db.get_product(product_id)
    print(f"Created product with ID: {product_id}, Retrieved product: {product}\n")

    updated = db.update_product(product_id, price=899.99, stock=15)
    product = db.get_product(product_id)
    print(f"Update product: {updated}, Retrieved product: {product}\n")

    deleted = db.delete_product(product_id)
    product = db.get_product(product_id)
    print(f"Delete product: {deleted}, Retrieved product: {product}\n")

    print("\n--- complex SQL query involving joins, aggregation, and sorting ---\n")

    # Get user orders
    print("Orders for user ID 1, using join query:")
    user_orders = db.get_user_orders(1)
    pprint(user_orders)
    print()

    # Get top selling products
    print("Top 3 selling products, using group by query:")
    top_products = db.get_top_selling_products(3)
    pprint(top_products)
    print()

    # Get user total spending
    print("Total spending for user ID 2, using sum and join query:")
    user_spending = db.get_user_total_spending(2)
    pprint(user_spending)
    print()

    # Get product sales by category
    print("Product sales by category, using group by query:")
    category_sales = db.get_product_sales_by_category()
    pprint(category_sales)
    print()

    # Get users with high balance
    print("Users with balance over 500, using where query:")
    high_balance_users = db.get_users_with_high_balance(900)
    pprint(high_balance_users)
    print()

    db.close()


if __name__ == "__main__":
    main()
