"""
@File    :  app.py
@Time    :  19/03/2023
@Author  :  Kerene Wright
@Version :  1.0
@Desc    : This program is a FLASK API implementation for the Customers database 

"""
from flask import Flask, request, make_response

import mysql.connector
import os
from dotenv import load_dotenv

# Get the database credentials
load_dotenv()

app = Flask(__name__)

# Database connection configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'auth_plugin': os.getenv('AUTH_PLUGIN')
}

@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        # cnx = mysql.connector.connect(user='klaw', password='kl@w1234', host='localhost', database='customers')
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute('SELECT * from Customers;')
        customers_list = []

        for CustomerID, Gender, Age, Annual_Income, Spending_Score, Profession, Work_Experience, Family_Size in cursor:
            customers = {}
            customers['Id'] = CustomerID
            customers['Gender'] = Gender
            customers['Age'] = Age
            customers['Annual Income'] = Annual_Income
            customers['Spending Score'] = Spending_Score
            customers['Profession'] = Profession
            customers['Work Experience'] = Work_Experience
            customers['Family Size'] = Family_Size

            customers_list.append(customers)
        cursor.close()
        cnx.close()
        return make_response(customers_list, 200)
    
    except Exception as e:
        return make_response({'error': str(e)}, 400)


@app.route('/customer/<customer_id>', methods=['GET'])
def get_customers_id(customer_id):
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        cursor.execute(f"SELECT * from Customers WHERE CustomerID={customer_id};")
        row = cursor.fetchone()
        customers = {}

        if row is not None:
            CustomerID, Gender, Age, Annual_Income, Spending_Score, Profession, Work_Experience, Family_Size = row
            customers = {}
            customers['Id'] = CustomerID
            customers['Gender'] = Gender
            customers['Age'] = Age
            customers['Annual Income'] = Annual_Income
            customers['Spending Score'] = Spending_Score
            customers['Profession'] = Profession
            customers['Work Experience'] = Work_Experience
            customers['Family Size'] = Family_Size
            cursor.close()
            cnx.close()
            return make_response(customers, 200)
        else:
            return make_response({'error': 'Customer not found'}, 400)
    except:
        return make_response({'error': 'An error has occured'}, 400)


@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        # cnx = mysql.connector.connect(user='klaw', password='kl@w1234', host='localhost', database='customers')
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        #json way of accepting data
        content = request.json
        CustomerID = content['CustomerID']
        Gender = content['Gender']
        Age = content['Age']
        Annual_Income = content['Annual_Income']
        Spending_Score = content['Spending_Score']
        Profession = content['Profession']
        Work_Experience = content['Work_Experience']
        Family_Size = content['Family_Size']

        #Form way of accepting a customer
        # CustomerID = request.form.get('CustomerID')
        # Gender = request.form.get('Gender')
        # Age = request.form.get('Age')
        # Annual_Income = request.form.get('Annual_Income')
        # Spending_Score = request.form.get('Spending_Score')
        # Profession = request.form.get('Profession')
        # Work_Experience = request.form.get('Work_Experience')
        # Family_Size = request.form.get('Family_Size')

        cursor.execute(f"INSERT INTO Customers VALUES('{CustomerID}', '{Gender}','{Age}','{Annual_Income}','{Spending_Score}','{Profession}','{Work_Experience}','{Family_Size}');")
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success" : "Customer added"}, 200)
    
    except Exception as e:
        print(e)
        return make_response({'error': 'An error has occured when adding a customer'}, 400)
    
@app.route('/update_profession/<customer_id>', methods=['PUT'])
def update_profession_id(customer_id):
    try:
        # cnx = mysql.connector.connect(user='klaw', password='kl@w1234', host='localhost', database='customers')
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        #json way of accepting data
        content = request.json
        Profession = content['Profession']

        cursor.execute(f"UPDATE Customers SET Profession = '{Profession}' WHERE CustomerID = {customer_id};")
        cnx.commit()
        cursor.close()
        cnx.close()
        return make_response({"success" : "Profession Updated"}, 200)
    
    except Exception as e:
        return make_response({'error': str(e)}, 400)
    
# can use a sub query to get the highest and then use the query to match to the customer id
@app.route('/highest_income_report', methods=['GET'])
def profession_highest_income():
    try:
        # cnx = mysql.connector.connect(user='klaw', password='kl@w1234', host='localhost', database='customers')
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        cursor.execute(f"SELECT CustomerID, MAX(Annual_Income) AS AnnualIncome, Profession FROM Customers GROUP BY CustomerID, Profession;")
        customers_list = []

        for CustomerID, AnnualIncome, Profession in cursor:
            customers = {}
            customers['CustomerID'] = CustomerID
            customers['AnnualIncome'] = AnnualIncome
            customers['Profession'] = Profession

            customers_list.append(customers)
        cursor.close()
        cnx.close()
        return make_response(customers_list, 200)
    
    except:
        return make_response({'error': 'An error has occured when retrieving highest income by profession'}, 400)
    


@app.route('/total_income_report', methods=['GET'])
def get_income_report():
    try:
        # cnx = mysql.connector.connect(user='klaw', password='kl@w1234', host='localhost', database='customers')
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        cursor.execute('SELECT SUM(Annual_Income) AS TotalIncome, Profession FROM Customers GROUP BY Profession;')
        customers_list = []

        for TotalIncome, Profession in cursor:
            customers = {}
            customers['TotalIncome'] = TotalIncome
            customers['Profession'] = Profession

            customers_list.append(customers)
        cursor.close()
        cnx.close()
        return make_response(customers_list, 200)
    
    except:
        return make_response({'error': 'An error has occured when retrieving total income report by profession'}, 400)
     

@app.route('/average_work_experience', methods=['GET'])
def avg_work_experience():
    try:
        # cnx = mysql.connector.connect(user='klaw', password='kl@w1234', host='localhost', database='customers')
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        cursor.execute(f"SELECT ROUND(AVG(Work_Experience),0) AS AVGExperience, Profession FROM Customers WHERE Annual_Income > 50000 AND Age < 35 GROUP BY Profession;")
        customers_list = []

        for AVGExperience, Profession in cursor:
            customers = {}
            customers['AVGExperience'] = AVGExperience
            customers['Profession'] = Profession

            customers_list.append(customers)
        cursor.close()
        cnx.close()
        return make_response(customers_list, 200)
    
    except Exception as e:
        return make_response({'error': 'An error has occured when getting the average work experience by profession'}, 400)
    

@app.route('/average_spending_score/<profession>', methods=['GET'])
def avg_spend_score(profession):
    try:
        cnx = mysql.connector.connect(**db_config)
        # cnx = mysql.connector.connect(user='klaw', password='kl@w1234', host='localhost', database='customers')
        cursor = cnx.cursor()

        cursor.execute(f"SELECT ROUND(AVG(Spending_Score),0) AS AVG_SpendScore, Gender FROM Customers WHERE Profession = '{profession}' GROUP BY Gender;")
        customers_list = []

        for AVG_SpendScore, Gender in cursor:
            customers = {}
            customers['AVG_SpendScore'] = AVG_SpendScore
            customers['Gender'] = Gender

            customers_list.append(customers)
        cursor.close()
        cnx.close()
        return make_response(customers_list, 200)
    
    except Exception as e:
        return make_response({'error': 'An error has occured when getting the average spending score by gender'}, 400)
