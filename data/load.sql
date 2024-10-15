.mode csv

.import './data/users.csv' users
.import './data/products.csv' products
.import './data/orders.csv' orders

UPDATE sqlite_sequence
SET seq = (
        SELECT MAX(user_id)
        FROM users
    )
WHERE name = 'users';

UPDATE sqlite_sequence
SET seq = (
        SELECT MAX(product_id)
        FROM products
    )
WHERE name = 'products';

UPDATE sqlite_sequence
SET seq = (
        SELECT MAX(order_id)
        FROM orders
    )
WHERE name = 'orders';

.echo on
SELECT 'Users count:',
    COUNT(*)
FROM users;
SELECT 'Products count:',
    COUNT(*)
FROM products;
SELECT 'Orders count:',
    COUNT(*)
FROM orders;
.echo off