import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="crud_python_db",
)

cursor = connection.cursor()

# # CREATE
# product_name = "Celular"
# price = 1100

# query = f'INSERT INTO sales (name, price) VALUES("{product_name}","{price}")'
# cursor.execute(query)

# connection.commit()  # when you want to edit the database
# # or result = cursor.fetchall()  # when you want to get data from thedatabase

# # READ

# query = "SELECT * FROM sales"
# cursor.execute(query)

# # connection.commit()  # when you want to edit the database
# result = cursor.fetchall()  # when you want to get data from the database
# print(result)

# # UPDATE

# name = "Açaí"
# price = 1200
# query = f'UPDATE sales SET name="{name}", price=1200 WHERE id=1'
# cursor.execute(query)
# connection.commit()

# DELETE

query = "DELETE FROM sales WHERE id=1"
cursor.execute(query)
connection.commit()


cursor.close()
connection.close()
