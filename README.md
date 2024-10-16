[![CI](https://github.com/bionicotaku/Evan_Li_IDS706_Hwk7/actions/workflows/cicd.yml/badge.svg)](https://github.com/bionicotaku/Evan_Li_IDS706_Hwk7/actions/workflows/cicd.yml)

## Evan_Li_IDS706_Hwk7

### File Structure

```
Evan_Li_IDS706_Hwk7/
├── .devcontainer/
│ ├── devcontainer.json
│ └── Dockerfile
├── .github/
│ └── workflows/cicd.yml
├── .gitignore
├── data/
│ ├── create.sql
│ └── awsec2.pem
├── LICENSE
├── main.py
├── Makefile
├── mylib/
│ ├── gen.py    -> generate sample data
│ ├── setup.py  -> create database and load data
│ └── CRUD.py   -> SQL query operations
├── README.md
├── requirements.txt
└── test_main.py
```

## Introduction

This project demonstrates a comprehensive database management system using AWS RDS MySQL as the backend. It establishes a secure connection to the database through an EC2 instance acting as a bastion host, utilizing SSH tunneling.

The system implements a three-table schema (Users, Products, and Orders) and showcases various database operations including:

1. Basic CRUD (Create, Read, Update, Delete) operations on Users and Products tables.
2. Complex SQL queries involving joins, aggregations, and sorting.
3. Sample data generation and database setup scripts.

The connection to the AWS RDS MySQL database is established using the following method:
1. SSH into an EC2 instance using a private key (.pem file).
2. Create an SSH tunnel from the EC2 instance to the RDS MySQL database.
3. Connect to the database through this secure tunnel using PyMySQL.

## Preparation

1. Install all the packages `make install`
2. Format code `make format`
3. Lint code `make lint`
4. Test coce `make test`

## Setup and Query

1. Create database, generate sample data and load  `make setup`, after that all procedure files are deleted automatically
2. Test all the query operations `make run`, including CRUD and complex SQL query involving joins, aggregation, and sorting. All the process detail will be printed

## Database Schema

This database consists of three main tables: Users, Products, and Orders.

### Users Table

Stores information about users.

| Column    | Type         | Constraints                |
|-----------|--------------|----------------------------|
| user_id   | INT          | PRIMARY KEY, AUTO_INCREMENT|
| email     | VARCHAR(255) | UNIQUE, NOT NULL           |
| firstname | VARCHAR(100) | NOT NULL                   |
| lastname  | VARCHAR(100) | NOT NULL                   |
| address   | TEXT         | NOT NULL                   |
| balance   | DECIMAL(10,2)| DEFAULT 0, NOT NULL        |

### Products Table

Contains details about available products.

| Column       | Type         | Constraints                |
|--------------|--------------|----------------------------|
| product_id   | INT          | PRIMARY KEY, AUTO_INCREMENT|
| product_name | VARCHAR(255) | NOT NULL                   |
| category     | VARCHAR(100) | NOT NULL                   |
| price        | DECIMAL(10,2)| NOT NULL, CHECK (price >= 0)|
| stock        | INT          | NOT NULL, CHECK (stock >= 0)|

### Orders Table

Tracks orders made by users.

| Column     | Type     | Constraints                |
|------------|----------|----------------------------|
| order_id   | INT      | PRIMARY KEY, AUTO_INCREMENT|
| user_id    | INT      | NOT NULL, FOREIGN KEY      |
| product_id | INT      | NOT NULL, FOREIGN KEY      |
| quantity   | INT      | NOT NULL, CHECK (quantity > 0)|
| order_date | DATETIME | NOT NULL                   |

Foreign Key Relationships:
- `orders.user_id` references `users.user_id`
- `orders.product_id` references `products.product_id`

## Query Operations

This project implements the following basic CRUD (Create, Read, Update, Delete) operations and complex queries:

### Basic CRUD Operations

1. User table operations:
   - Create user: `create_user()`
   - Get user information: `get_user()`
   - Update user information: `update_user()`
   - Delete user: `delete_user()`

2. Product table operations:
   - Create product: `create_product()`
   - Get product information: `get_product()`
   - Update product information: `update_product()`
   - Delete product: `delete_product()`

### Detailed Complex Queries

1. Get User Orders:
   ```sql
   SELECT o.order_id, p.product_name, o.quantity, o.order_date, 
          (p.price * o.quantity) as total_price
   FROM orders o
   JOIN products p ON o.product_id = p.product_id
   WHERE o.user_id = %s
   ORDER BY o.order_date DESC
   ```
   This query joins the orders and products tables to retrieve detailed order information for a specific user, including the calculated total price for each order.

2. Get Top Selling Products:
   ```sql
   SELECT p.product_id, p.product_name, SUM(o.quantity) as total_sold
   FROM products p
   JOIN orders o ON p.product_id = o.product_id
   GROUP BY p.product_id, p.product_name
   ORDER BY total_sold DESC
   LIMIT %s
   ```
   This query aggregates the total quantity sold for each product, orders them by the total sold in descending order, and limits the results to a specified number of top-selling products.

3. Get User Total Spending:
   ```sql
   SELECT u.user_id, u.email, SUM(p.price * o.quantity) as total_spending
   FROM users u
   JOIN orders o ON u.user_id = o.user_id
   JOIN products p ON o.product_id = p.product_id
   WHERE u.user_id = %s
   GROUP BY u.user_id, u.email
   ```
   This query calculates the total spending of a specific user by joining the users, orders, and products tables, and summing the product of price and quantity for all orders.

4. Get Product Sales by Category:
   ```sql
   SELECT p.category, SUM(o.quantity) as total_sold,
          SUM(p.price * o.quantity) as total_revenue
   FROM products p
   JOIN orders o ON p.product_id = o.product_id
   GROUP BY p.category
   ORDER BY total_revenue DESC
   ```
   This query aggregates sales data by product category, calculating both the total quantity sold and the total revenue for each category.

5. Get Users with High Balance:
   ```sql
   SELECT user_id, email, firstname, lastname, balance
   FROM users
   WHERE balance > %s
   ORDER BY balance DESC
   ```
   This query retrieves users whose balance exceeds a specified threshold, ordering the results by balance in descending order.
