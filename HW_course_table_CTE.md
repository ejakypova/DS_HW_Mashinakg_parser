Д\З:
1) Создать таблицу курсы с полями и данными
поля: id  INT, course_name VARCHAR(100), price DECIMAL(10,2), mentor_id INT
2) Создайте CTE expensive_courses, которое содержит курсы дороже 15000.
3) Создайте CTE avarage_cost, которое вычисляет среднюю стоимость курсов
4) Создайте CTE max_price, которое вычисляет максимальную стоимость
5) Создайте CTE min_price, которое вычисляет минимальную стоимость
6) Создайте CTE mentor_courses, которое содержит все курсы ментора с mentor_id = 1

# ================ Создать таблицу курсы с полями и данными
# поля: id  INT, course_name VARCHAR(100), price DECIMAL(10,2), mentor_id INT

===================== Создала таблицу =========================================
CREATE TABLE course_table(
    -> id INT,
    -> course_name VARCHAR(100),
    -> price DECIMAL (10,2),
    -> mentor_id INT
    -> );
Query OK, 0 rows affected (0.779 sec)

 SHOW TABLES;
+-------------------+
| Tables_in_courses |
+-------------------+
| course_table      |
| courses_list      |
| employes          |
| mentors           |
| students          |
+-------------------+

===================== Внесла данные в талицу =========================================

INSERT INTO course_table (id, course_name, price, mentor_id)
    -> VALUES (1, 'Python', 15000, 2),
    -> (2, 'Java', 25000, 1),
    -> (3, 'C#', 30000, 2),
    -> (4, 'SQL', 18000, 3),
    -> (5, 'PHP', 35000, 4);
Query OK, 5 rows affected (0.161 sec)
Records: 5  Duplicates: 0  Warnings: 0

SELECT * FROM course_table;
+------+-------------+----------+-----------+
| id   | course_name | price    | mentor_id |
+------+-------------+----------+-----------+
|    1 | Python      | 15000.00 |         2 |
|    2 | Java        | 25000.00 |         1 |
|    3 | C#          | 30000.00 |         2 |
|    4 | SQL         | 18000.00 |         3 |
|    5 | PHP         | 35000.00 |         4 |
+------+-------------+----------+-----------+

# Создайте CTE expensive_courses, которое содержит курсы дороже 15000.
    WITH expensive_courses AS
    -> (
    -> SELECT *FROM course_table WHERE price > 15000
    -> )
    -> SELECT * FROM expensive_courses;
+------+-------------+----------+-----------+
| id   | course_name | price    | mentor_id |
+------+-------------+----------+-----------+
|    2 | Java        | 25000.00 |         1 |
|    3 | C#          | 30000.00 |         2 |
|    4 | SQL         | 18000.00 |         3 |
|    5 | PHP         | 35000.00 |         4 |
+------+-------------+----------+-----------+

# Создайте CTE avarage_cost, которое вычисляет среднюю стоимость курсов

SELECT AVG(price) AS avarage_cost FROM course_table;
+--------------+
| avarage_cost |
+--------------+
| 24600.000000 |
+--------------+

# Создайте CTE max_price, которое вычисляет максимальную стоимость

 SELECT MAX(price) AS max_price FROM course_table;
+-----------+
| max_price |
+-----------+
|  35000.00 |
+-----------+

# Создайте CTE min_price, которое вычисляет минимальную стоимость

SELECT MIN(price) AS min_price FROM course_table;
+-----------+
| min_price |
+-----------+
|  15000.00 |
+-----------+

# Создайте CTE mentor_courses, которое содержит все курсы ментора с mentor_id = 1

 WITH mentor_courses AS
    -> (
    -> SELECT * FROM course_table WHERE mentor_id = 1
    -> )
    -> SELECT * FROM mentor_courses;
+------+-------------+----------+-----------+
| id   | course_name | price    | mentor_id |
+------+-------------+----------+-----------+
|    2 | Java        | 25000.00 |         1 |
+------+-------------+----------+-----------+
1 row in set (0.021 sec)