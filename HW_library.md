# Д/З
1. Создать БД Library
2. Создать записи books
3. Добавить как минимум 3 записи
4. Выполнить:
    4.1. SELECT
    4.2. UPDATE
    4.3. DELETE
     (Необходимо md файл закинуть в гитхаб)

=========================================== Создать БД Library ==============================================

    CREATE DATABASE library1;
Query OK, 1 row affected (0.166 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| courses            |
| information_schema |
| library1           |
| mentors            |
| my_library         |
| mysql              |
| performance_schema |
| sakila             |
| scholl             |
| sys                |
| world              |
+--------------------+

=========================================== Создать записи books ==============================================

mysql> CREATE TABLE books (
    -> id INT PRIMARY KEY,
    -> name VARCHAR(255),
    -> language VARCHAR(50),
    -> author VARCHAR (255),
    -> numb_pages INT
    -> );
Query OK, 0 rows affected (0.522 sec)

mysql> SHOW TABLES;
+--------------------+
| Tables_in_library1 |
+--------------------+
| books              |
+--------------------+

======================================= Добавить как минимум 3 записи =========================================

mysql> INSERT INTO books
    -> VALUES (2, 'Статистика и котики', 'Русский', 'Владимир Савельев', 182),
    -> (3, 'Атомные привычки', 'Русский', 'Джеймс Клир', 304),
    -> (4, 'Как привести дела в порядок', 'Русский', 'Дэвид Аллен', 416);
Query OK, 3 rows affected (0.066 sec)
Records: 3  Duplicates: 0  Warnings: 0

 INSERT INTO books
    ->  VALUE (10, "Dumai medlenno, reshai bystro", "RU", "D. Kaneman", 656);
Query OK, 1 row affected (0.066 sec)

mysql> SELECT * FROM books;
+----+-------------------------------+----------+-------------------+------------+
| id | name                          | language | author            | numb_pages |
+----+-------------------------------+----------+-------------------+------------+
|  5 | ????? ????????, ????? ??????  | ???????  | ??????? ???????   |        656 |
|  6 | ?????????? ? ??????           | ???????  | ???????? ???????? |        182 |
|  7 | ??????? ????????              | ???????  | ?????? ????       |        304 |
|  8 | ??? ???????? ???? ? ???????   | ???????  | ????? ?????       |        416 |
|  9 | ????? ????????, ????? ??????  | ???????  | ??????? ???????   |        656 |
| 10 | Dumai medlenno, reshai bystro | RU       | D. Kaneman        |        656 |
+----+-------------------------------+----------+-------------------+------------+
6 rows in set (0.023 sec)

mysql> INSERT INTO books
    -> VALUES  (11, 'Statistika i kotiki', 'RU', 'V. Saveliev', 182),
    ->  (12, 'Atomnye privychki', 'RU', 'D. Klir', 304),
    -> (13, 'Kak privesti dela v poryadok', 'RU', 'D. Allen', 416);
Query OK, 3 rows affected (0.067 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM books;
+----+-------------------------------+----------+-------------------+------------+
| id | name                          | language | author            | numb_pages |
+----+-------------------------------+----------+-------------------+------------+
|  5 | ????? ????????, ????? ??????  | ???????  | ??????? ???????   |        656 |
|  6 | ?????????? ? ??????           | ???????  | ???????? ???????? |        182 |
|  7 | ??????? ????????              | ???????  | ?????? ????       |        304 |
|  8 | ??? ???????? ???? ? ???????   | ???????  | ????? ?????       |        416 |
|  9 | ????? ????????, ????? ??????  | ???????  | ??????? ???????   |        656 |
| 10 | Dumai medlenno, reshai bystro | RU       | D. Kaneman        |        656 |
| 11 | Statistika i kotiki           | RU       | V. Saveliev       |        182 |
| 12 | Atomnye privychki             | RU       | D. Klir           |        304 |
| 13 | Kak privesti dela v poryadok  | RU       | D. Allen          |        416 |
+----+-------------------------------+----------+-------------------+------------+



===================================== Выполнить: SELECT, UPDATE, DELETE =======================================
# ============================================ SELECT =========================================================
mysql> SELECT * FROM books;
+----+------------------------------+----------+-------------------+------------+
| id | name                         | language | author            | numb_pages |
+----+------------------------------+----------+-------------------+------------+
|  1 | ????? ????????, ????? ?????? | ???????  | ??????? ???????   |        656 |
|  2 | ?????????? ? ??????          | ???????  | ???????? ???????? |        182 |
|  3 | ??????? ????????             | ???????  | ?????? ????       |        304 |
|  4 | ??? ???????? ???? ? ???????  | ???????  | ????? ?????       |        416 |
+----+------------------------------+----------+-------------------+------------+


mysql> SELECT * FROM books;
+----+-------------------------------+----------+-------------------+------------+
| id | name                          | language | author            | numb_pages |
+----+-------------------------------+----------+-------------------+------------+
|  5 | ????? ????????, ????? ??????  | ???????  | ??????? ???????   |        656 |
|  6 | ?????????? ? ??????           | ???????  | ???????? ???????? |        182 |
|  7 | ??????? ????????              | ???????  | ?????? ????       |        304 |
|  8 | ??? ???????? ???? ? ???????   | ???????  | ????? ?????       |        416 |
|  9 | ????? ????????, ????? ??????  | ???????  | ??????? ???????   |        656 |
| 10 | Dumai medlenno, reshai bystro | RU       | D. Kaneman        |        656 |
| 11 | Statistika i kotiki           | RU       | V. Saveliev       |        182 |
| 12 | Atomnye privychki             | RU       | D. Klir           |        304 |
| 13 | Kak privesti dela v poryadok  | RU       | D. Allen          |        416 |
+----+-------------------------------+----------+-------------------+------------+

# ============================================ UPDATE =========================================================
UPDATE books
    -> SET name = 'Ubit pereseshnika',
    ->          language = 'RU',
    ->          author = 'H. Li'
    -> WHERE id = 8;
Query OK, 1 row affected (0.148 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT *FROM books;
+----+-------------------------------+----------+-------------------+------------+
| id | name                          | language | author            | numb_pages |
+----+-------------------------------+----------+-------------------+------------+
|  5 | ????? ????????, ????? ??????  | ???????  | ??????? ???????   |        656 |
|  6 | ?????????? ? ??????           | ???????  | ???????? ???????? |        182 |
|  7 | ??????? ????????              | ???????  | ?????? ????       |        304 |
|  8 | Ubit pereseshnika             | RU       | H. Li             |        416 |
|  9 | ????? ????????, ????? ??????  | ???????  | ??????? ???????   |        656 |
| 10 | Dumai medlenno, reshai bystro | RU       | D. Kaneman        |        656 |
| 11 | Statistika i kotiki           | RU       | V. Saveliev       |        182 |
| 12 | Atomnye privychki             | RU       | D. Klir           |        304 |
| 13 | Kak privesti dela v poryadok  | RU       | D. Allen          |        416 |
+----+-------------------------------+----------+-------------------+------------+
9 rows in set (0.036 sec)

# ============================================ DELETE =========================================================

 DELETE FROM books
    -> WHERE id = 3;
Query OK, 0 rows affected (0.039 sec)

mysql>  DELETE FROM books
    ->  WHERE  id IN (1, 2, 4, 5, 6, 9);
Query OK, 3 rows affected (0.101 sec)

mysql> SELECT *FROM books;
+----+-------------------------------+----------+-------------+------------+
| id | name                          | language | author      | numb_pages |
+----+-------------------------------+----------+-------------+------------+
|  7 | ??????? ????????              | ???????  | ?????? ???? |        304 |
|  8 | Ubit pereseshnika             | RU       | H. Li       |        416 |
| 10 | Dumai medlenno, reshai bystro | RU       | D. Kaneman  |        656 |
| 11 | Statistika i kotiki           | RU       | V. Saveliev |        182 |
| 12 | Atomnye privychki             | RU       | D. Klir     |        304 |
| 13 | Kak privesti dela v poryadok  | RU       | D. Allen    |        416 |
+----+-------------------------------+----------+-------------+------------+
6 rows in set (0.010 sec)

mysql> DELETE FROM books
    ->     -> WHERE id = 7;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '-> WHERE id = 7' at line 2
mysql> DELETE FROM books
    -> WHERE id = 7;
Query OK, 1 row affected (0.067 sec)

mysql>  SELECT *FROM books;
+----+-------------------------------+----------+-------------+------------+
| id | name                          | language | author      | numb_pages |
+----+-------------------------------+----------+-------------+------------+
|  8 | Ubit pereseshnika             | RU       | H. Li       |        416 |
| 10 | Dumai medlenno, reshai bystro | RU       | D. Kaneman  |        656 |
| 11 | Statistika i kotiki           | RU       | V. Saveliev |        182 |
| 12 | Atomnye privychki             | RU       | D. Klir     |        304 |
| 13 | Kak privesti dela v poryadok  | RU       | D. Allen    |        416 |
+----+-------------------------------+----------+-------------+------------+
5 rows in set (0.011 sec)