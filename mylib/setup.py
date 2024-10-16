import subprocess
import os
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
            print("Connecting to EC2 instance...")
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

            print("Connecting to MySQL database...")
            self.conn = pymysql.connect(
                host='127.0.0.1',
                port=self.tunnel.local_bind_port,
                user=self.db_username,
                password=self.db_password,
                connect_timeout=10,
                local_infile=1  # Add this line
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            print("Successfully connected to MySQL database")

            # Create database (if not exists)
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            self.conn.commit()

            # Switch to the specified database
            self.conn.select_db(self.db_name)
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
        print("All connections closed")


def run_sql_create_file(db, file_path):
    """Execute a SQL file using MySQL"""
    try:
        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()
            # Split the script into individual statements
            statements = sql_script.split(';')
            for statement in statements:
                # Skip empty statements
                if statement.strip():
                    db.cursor.execute(statement)
        db.conn.commit()
        print(f"Successfully executed {file_path}")
    except pymysql.Error as e:
        print(f"Error executing {file_path}: {e}")
        exit(1)


def run_python_script(script_path):
    """Run a Python script"""
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"Successfully ran {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
        exit(1)


def delete_csv_files(directory):
    """Delete all CSV files in the specified directory"""
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            try:
                os.remove(file_path)
                print(f"Deleted {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")


def create_database(db):
    """Create the MySQL database tables if they don't exist"""
    try:
        tables = ['orders', 'products','users']
        for table in tables:
            db.cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"Dropped table '{table}' if it existed.")
        db.conn.commit()
        print("Database tables reset")
    except pymysql.Error as e:
        print(f"Error resetting database tables: {e}")
        exit(1)


def load_csv_to_database(db, csv_file, table_name):
    try:
        with open(csv_file, 'r') as file:
            csv_data = file.read()
            csv_data = csv_data.replace("'", "''")  # Escape single quotes
            db.cursor.execute(f"""
                LOAD DATA LOCAL INFILE '{csv_file}'
                INTO TABLE {table_name}
                FIELDS TERMINATED BY ','
                ENCLOSED BY '"'
                LINES TERMINATED BY '\\n'
                IGNORE 0 ROWS
            """)
        db.conn.commit()
        if db.cursor.rowcount > 0:
            print(f"Successfully imported data from {csv_file} to {table_name} table")
        else:
            print(f"No data imported from {csv_file} to {table_name} table")
    except pymysql.Error as e:
        print(f"Error importing data from {csv_file} to {table_name} table: {e}")
        exit(1)


def setup_database():
    db = Database()

    try:
        # Step 1: Reset the database tables
        create_database(db)

        # Step 2: Create or update the database schema
        run_sql_create_file(db, "./data/create.sql")

        # Step 3: Generate sample data
        run_python_script("./mylib/gen.py")

        # Step 4: Load data into the database directly from CSV files
        load_csv_to_database(db, "./data/users.csv", "users")
        load_csv_to_database(db, "./data/products.csv", "products")
        load_csv_to_database(db, "./data/orders.csv", "orders")

        # Step 5: Delete CSV files
        delete_csv_files("./data")

        print("\nDatabase setup complete, and all sample data has been created.")
    finally:
        db.close()


if __name__ == "__main__":
    setup_database()
