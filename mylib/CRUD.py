import pymysql
import sshtunnel
from pathlib import Path


class Database:
    def __init__(self):
        # SSH configuration
        self.ssh_host = "ec2-3-21-207-62.us-east-2.compute.amazonaws.com"
        self.ssh_port = 22
        self.ssh_username = "ubuntu"
        self.ssh_pkey = Path("data/awsec2.pem").expanduser()

        # Database configuration
        self.db_host = "database-ids706.c54m20ukqi03.us-east-2.rds.amazonaws.com"
        self.db_port = 3306
        self.db_username = "admin"
        self.db_password = "31415926"
        self.db_name = "mydb"

        self.tunnel = None
        self.conn = None
        self.cursor = None

        self.connect()

    def connect(self):
        try:
            print("Starting database connection...")
            if not Path(self.ssh_pkey).exists():
                raise FileNotFoundError(f"SSH key file does not exist: {self.ssh_pkey}")
            
            self.tunnel = sshtunnel.SSHTunnelForwarder(
                (self.ssh_host, self.ssh_port),
                ssh_username=self.ssh_username,
                ssh_pkey=str(self.ssh_pkey),
                remote_bind_address=(self.db_host, self.db_port)
            )
            self.tunnel.start()
            print(f"SSH tunnel established, local port: {self.tunnel.local_bind_port}")

            self.conn = pymysql.connect(
                host='127.0.0.1',
                port=self.tunnel.local_bind_port,
                user=self.db_username,
                password=self.db_password,
                db=self.db_name,
                connect_timeout=10,
                local_infile=1
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            print(f"Connected to database: {self.db_name}")

        except Exception as e:
            print(f"Connection error: {e}")
            self.close()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if self.tunnel:
            self.tunnel.stop()
        print("Database connection closed")

    # User CRUD operations
    def create_user(self, email, firstname, lastname, address, balance=0):
        sql = '''INSERT INTO users (email, firstname, lastname, address, balance)
                 VALUES (%s, %s, %s, %s, %s)'''
        self.cursor.execute(
            sql, (email, firstname, lastname, address, balance))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user(self, user_id):
        sql = 'SELECT * FROM users WHERE user_id = %s'
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchone()

    def update_user(self, user_id, email=None, firstname=None,
                    lastname=None, address=None, balance=None):
        updates = []
        values = []
        if email is not None:
            updates.append('email = %s')
            values.append(email)
        if firstname is not None:
            updates.append('firstname = %s')
            values.append(firstname)
        if lastname is not None:
            updates.append('lastname = %s')
            values.append(lastname)
        if address is not None:
            updates.append('address = %s')
            values.append(address)
        if balance is not None:
            updates.append('balance = %s')
            values.append(balance)

        if not updates:
            return False

        sql = f'UPDATE users SET {", ".join(updates)} WHERE user_id = %s'
        values.append(user_id)
        self.cursor.execute(sql, tuple(values))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_user(self, user_id):
        sql = 'DELETE FROM users WHERE user_id = %s'
        self.cursor.execute(sql, (user_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # Product CRUD operations
    def create_product(self, product_name, category, price, stock):
        sql = '''INSERT INTO products (product_name, category, price, stock)
                 VALUES (%s, %s, %s, %s)'''
        self.cursor.execute(sql, (product_name, category, price, stock))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_product(self, product_id):
        sql = 'SELECT * FROM products WHERE product_id = %s'
        self.cursor.execute(sql, (product_id,))
        return self.cursor.fetchone()

    def update_product(self, product_id, product_name=None,
                       category=None, price=None, stock=None):
        updates = []
        values = []
        if product_name is not None:
            updates.append('product_name = %s')
            values.append(product_name)
        if category is not None:
            updates.append('category = %s')
            values.append(category)
        if price is not None:
            updates.append('price = %s')
            values.append(price)
        if stock is not None:
            updates.append('stock = %s')
            values.append(stock)

        if not updates:
            return False

        sql = f'UPDATE products SET {", ".join(updates)} WHERE product_id = %s'
        values.append(product_id)
        self.cursor.execute(sql, tuple(values))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_product(self, product_id):
        sql = 'DELETE FROM products WHERE product_id = %s'
        self.cursor.execute(sql, (product_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_user_orders(self, user_id):
        sql = '''
        SELECT o.order_id, p.product_name, o.quantity, o.order_date, 
               (p.price * o.quantity) as total_price
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.user_id = %s
        ORDER BY o.order_date DESC
        '''
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchall()

    def get_top_selling_products(self, limit=5):
        sql = '''
        SELECT p.product_id, p.product_name, SUM(o.quantity) as total_sold
        FROM products p
        JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_sold DESC
        LIMIT %s
        '''
        self.cursor.execute(sql, (limit,))
        return self.cursor.fetchall()

    def get_user_total_spending(self, user_id):
        sql = '''
        SELECT u.user_id, u.email, SUM(p.price * o.quantity) as total_spending
        FROM users u
        JOIN orders o ON u.user_id = o.user_id
        JOIN products p ON o.product_id = p.product_id
        WHERE u.user_id = %s
        GROUP BY u.user_id, u.email
        '''
        self.cursor.execute(sql, (user_id,))
        return self.cursor.fetchone()

    def get_product_sales_by_category(self):
        sql = '''
        SELECT p.category, SUM(o.quantity) as total_sold,
               SUM(p.price * o.quantity) as total_revenue
        FROM products p
        JOIN orders o ON p.product_id = o.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_users_with_high_balance(self, balance_threshold):
        sql = '''
        SELECT user_id, email, firstname, lastname, balance
        FROM users
        WHERE balance > %s
        ORDER BY balance DESC
        '''
        self.cursor.execute(sql, (balance_threshold,))
        return self.cursor.fetchall()
