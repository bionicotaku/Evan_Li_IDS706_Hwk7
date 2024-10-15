import subprocess
import os
import sqlite3

DB_FILE = './data/mydatabase.db'

def run_sql_create_file(file_path):
    """Execute a SQL file using SQLite"""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            with open(file_path, 'r') as sql_file:
                sql_script = sql_file.read()
                conn.executescript(sql_script)
        print(f"Successfully executed {file_path}")
    except sqlite3.Error as e:
        print(f"Error executing {file_path}: {e}")
        exit(1)
        
def run_sql_load_file(file_path):
    try:
        command = f"sqlite3 {DB_FILE} < {file_path}"
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True, check=True)
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing SQLite shell command: {e}")
        print(f"Error output: {e.stderr}")
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

def create_database():
    """Create the SQLite database file if it doesn't exist"""
    if not os.path.exists(DB_FILE):
        try:
            conn = sqlite3.connect(DB_FILE)
            tables = ['users', 'products', 'orders']
            for table in tables:
                conn.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"Dropped table '{table}' if it existed.")
            conn.close()
            print(f"Created new database file: {DB_FILE}")
        except sqlite3.Error as e:
            print(f"Error creating database file: {e}")
            exit(1)
    else:
        print(f"Database file {DB_FILE} already exists")

def setup_database():
    # Step 1: Create the database file
    create_database()

    # Step 2: Create or update the database schema
    run_sql_create_file("./data/create.sql")

    # Step 3: Generate sample data
    run_python_script("./mylib/gen.py")

    # Step 4: Load data into the database
    run_sql_load_file("./data/load.sql")

    # Step 5: Delete CSV files
    delete_csv_files("./data")

    print("\nDatabase setup and created all the example data.")
    
if __name__ == "__main__":
    setup_database()