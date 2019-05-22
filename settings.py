# In order to use MySQL Connector we need to import the connector property
# of the mysql module
import mysql.connector

site_title = "Car CRUD Application"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cars"
)

# To execute SQL queries we need to create a cursor
# We can set the dictionary parameter of the cursor() method to True
# in order to have rows returned as dictionaries
mycursor = mydb.cursor(dictionary=True, buffered=True)
