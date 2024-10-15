import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {db_name}")

    def close(self):
        self.conn.close()

    # User CRUD operations
    def create_user(self, email, firstname, lastname, address, balance=0):
        sql = '''INSERT INTO users (email, firstname, lastname, address, balance)
                 VALUES (?, ?, ?, ?, ?)'''
        self.cursor.execute(sql, (email, firstname, lastname, address, balance))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user(self, user_id):
        sql = 'SELECT * FROM users WHERE user_id = ?'
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchone()

    def update_user(self, user_id, email=None, firstname=None,
                    lastname=None, address=None, balance=None):
        updates = []
        values = []
        if email is not None:
            updates.append('email = ?')
            values.append(email)
        if firstname is not None:
            updates.append('firstname = ?')
            values.append(firstname)
        if lastname is not None:
            updates.append('lastname = ?')
            values.append(lastname)
        if address is not None:
            updates.append('address = ?')
            values.append(address)
        if balance is not None:
            updates.append('balance = ?')
            values.append(balance)
        
        if not updates:
            return False

        sql = f'UPDATE users SET {", ".join(updates)} WHERE user_id = ?'
        values.append(user_id)
        self.cursor.execute(sql, tuple(values))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_user(self, user_id):
        sql = 'DELETE FROM users WHERE user_id = ?'
        self.cursor.execute(sql, (user_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # Product CRUD operations
    def create_product(self, product_name, category, price, stock):
        sql = '''INSERT INTO products (product_name, category, price, stock)
                 VALUES (?, ?, ?, ?)'''
        self.cursor.execute(sql, (product_name, category, price, stock))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_product(self, product_id):
        sql = 'SELECT * FROM products WHERE product_id = ?'
        self.cursor.execute(sql, (product_id,))
        return self.cursor.fetchone()

    def update_product(self, product_id, product_name=None,
                       category=None, price=None, stock=None):
        updates = []
        values = []
        if product_name is not None:
            updates.append('product_name = ?')
            values.append(product_name)
        if category is not None:
            updates.append('category = ?')
            values.append(category)
        if price is not None:
            updates.append('price = ?')
            values.append(price)
        if stock is not None:
            updates.append('stock = ?')
            values.append(stock)
        
        if not updates:
            return False

        sql = f'UPDATE products SET {", ".join(updates)} WHERE product_id = ?'
        values.append(product_id)
        self.cursor.execute(sql, tuple(values))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_product(self, product_id):
        sql = 'DELETE FROM products WHERE product_id = ?'
        self.cursor.execute(sql, (product_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0