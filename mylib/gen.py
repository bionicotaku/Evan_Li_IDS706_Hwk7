import csv
from faker import Faker
import random

# Set up Faker
Faker.seed(0)
fake = Faker()

# Constants
NUM_USERS = 50
NUM_PRODUCTS = 100
NUM_ORDERS = 200

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_users(num_users):
    with open('./data/users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Generating Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = profile['address'].replace('\n', ', ')
            balance = round(random.uniform(0, 1000), 2)
            writer.writerow([uid + 1, email, firstname, lastname, address, balance])
        print(f'{num_users} generated')

def gen_products(num_products):
    categories = ['Electronics', 'Books', 'Clothing', 
                  'Household', 'Toys', 'Food', 'Sports']
    with open('./data/products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Generating Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 20 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            category = random.choice(categories)
            price = round(random.uniform(1, 1000), 2)
            stock = random.randint(0, 1000)
            writer.writerow([pid + 1, name, category, price, stock])
        print(f'{num_products} generated')

def gen_orders(num_orders, num_users, num_products):
    with open('./data/orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Generating Orders...', end=' ', flush=True)
        for oid in range(num_orders):
            if oid % 40 == 0:
                print(f'{oid}', end=' ', flush=True)
            user_id = random.randint(1, num_users)
            product_id = random.randint(1, num_products)
            quantity = random.randint(1, 10)
            order_date_temp = fake.date_time_between(start_date='-1y', end_date='now')
            order_date = order_date_temp.strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([oid + 1, user_id, product_id, quantity, order_date])
        print(f'{num_orders} generated')

if __name__ == '__main__':
    gen_users(NUM_USERS)
    gen_products(NUM_PRODUCTS)
    gen_orders(NUM_ORDERS, NUM_USERS, NUM_PRODUCTS)
    print("Sample data generation complete.")