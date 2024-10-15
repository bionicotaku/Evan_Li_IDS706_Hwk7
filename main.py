import mylib.CRUD as crud
import mylib.setup as setup

DB_FILE = './data/mydatabase.db'

def main():
    setup.setup_database()
    
    db = crud.Database(DB_FILE)

    # User CRUD examples on User table
    user_id = db.create_user("john@example.com", "John", "Doe", "123 Main St", 100)
    user = db.get_user(user_id)
    print(f"Created user with ID: {user_id}, Retrieved user: {user}")

    updated = db.update_user(user_id, email="johndoe@example.com", balance=200)
    user = db.get_user(user_id)
    print(f"Update user status: {updated}, Retrieved user: {user}")

    deleted = db.delete_user(user_id)
    user = db.get_user(user_id)
    print(f"Delete user status: {deleted}, Retrieved user: {user}")

    # Product CRUD examples on Product table
    product_id = db.create_product("Laptop", "Electronics", 999.99, 10)
    product = db.get_product(product_id)
    print(f"Created product with ID: {product_id}, Retrieved product: {product}")

    updated = db.update_product(product_id, price=899.99, stock=15)
    product = db.get_product(product_id)
    print(f"Update product: {updated}, Retrieved product: {product}")

    deleted = db.delete_product(product_id)
    product = db.get_product(product_id)
    print(f"Delete product: {deleted}, Retrieved product: {product}")

    db.close()

if __name__ == "__main__":
    main()