"""
This file is the code that will read the data in the .csv and insert the queries into the Customers Databse.
Upon Completion the data in the csv will be inserted into the database.

"""


import csv
import mysql.connector

# Connection to MySQL database
cnx = mysql.connector.connect(user='klaw', password='kl@w1234', host='localhost', database='customers')

cursor = cnx.cursor()

# Open the CSV file
with open('Customers.csv', 'r') as csvfile:
    
    # Create a CSV reader
    reader = csv.reader(csvfile)

    # Skip the header row
    next(reader)

    # Iterate over the rows in the CSV file
    for row in reader:
        # Extract the data from the row
        col1, col2, col3, col4, col5, col6, col7, col8 = row

        # Construct the SQL query
        query = "INSERT INTO Customers (CustomerID, Gender, Age, Annual_Income, Spending_Score, Profession, Work_Experience, Family_Size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        # Execute the query
        cursor.execute(query, (col1, col2, col3, col4, col5, col6, col7, col8))

# Commit the changes to the database
cnx.commit()

# Close the cursor and the connection
cursor.close()
cnx.close()
