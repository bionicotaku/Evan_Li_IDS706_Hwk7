[![CI](https://github.com/bionicotaku/Evan_Li_IDS706_Hwk7/actions/workflows/cicd.yml/badge.svg)](https://github.com/bionicotaku/Evan_Li_IDS706_Hwk7/actions/workflows/cicd.yml)

## Evan_Li_IDS706_Hwk7

### File Structure

    ```
Evan_Li_IDS706_Hwk7/
├── .devcontainer/
│   ├── devcontainer.json
│   └── Dockerfile
├── .github/
│   └── workflows/cicd.yml
├── .gitignore
├── data/
│   ├── create.sql
│   ├── load.sql
│   └── mydatabase.db   -> database
├── LICENSE
├── main.py
├── Makefile
├── mylib/
│   ├── gen.py          -> generate sample data
│   ├── setup.py        -> create database and load data
│   └── CRUD.py         -> CRUD operations
├── README.md
├── requirements.txt
└── test_main.py
    ```

## Intrduction

This project will first create a database with 3 tables, generate sample data and load. Then, it will test the create, read, update, delete operations.

## Preparation

1. Install all the packages `make install`
2. Format code `make format`
3. Lint code `make lint`
4. Test coce `make test`

## CRUD

1. Create database, generate sample data and load  `make database-setup`
2. Test CRUD operations `make run-crud`, all the process detail will be printed

## Database Schema

This database consists of three main tables: Users, Products, and Orders.

### Users Table

Stores information about users.

| Column    | Type    | Constraints                |
|-----------|---------|----------------------------|
| user_id   | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| email     | TEXT    | UNIQUE, NOT NULL           |
| firstname | TEXT    | NOT NULL                   |
| lastname  | TEXT    | NOT NULL                   |
| address   | TEXT    | NOT NULL                   |
| balance   | REAL    | DEFAULT 0, NOT NULL        |

### Products Table

Contains details about available products.

| Column       | Type    | Constraints                |
|--------------|---------|----------------------------|
| product_id   | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| product_name | TEXT    | NOT NULL                   |
| category     | TEXT    | NOT NULL                   |
| price        | REAL    | NOT NULL, CHECK (price >= 0) |
| stock        | INTEGER | NOT NULL, CHECK (stock >= 0) |

### Orders Table

Tracks orders made by users.

| Column     | Type    | Constraints                |
|------------|---------|----------------------------|
| order_id   | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| user_id    | INTEGER | NOT NULL, FOREIGN KEY      |
| product_id | INTEGER | NOT NULL, FOREIGN KEY      |
| quantity   | INTEGER | NOT NULL, CHECK (quantity > 0) |
| order_date | TEXT    | NOT NULL                   |
