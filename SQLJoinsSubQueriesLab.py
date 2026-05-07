#!/usr/bin/env python
# coding: utf-8

# ## Introduction
# 
# In this lab assessment, you'll practice your knowledge of JOIN statements and subqueries, using various types of joins and various methods for specifying the links between them. One of the main benefits of using a relational database is the table relations that define them which allow you to access and connect data together via shared columns. By writing more advanced SQL queries that utilize joins and subqueries you can provide a deeper and more granular level of analysis and data retrieval.
# 
# This assessment will continue looking at the familiar Northwind database that contains customer relationship management (CRM) data as well as employee and product data. You will take a deeper dive into this database in order to accomplish more advanced SQL queries that require you to access data from multiple tables at once. 
# 
# Imagine that you are working in an analyst role for the sales rep team. They have collaborated with the customer relations and the product teams to take a comprehensive look at the employee to customer pipeline in an attempt to find areas of improvement and potential growth. You have been asked to provide some specific data and statistics regarding this project.

# ## Learning Objectives
# 
# You will be able to:
# 
# * Write SQL queries that make use of various types of joins
# * Choose and perform whichever type of join is best for retrieving desired data
# * Write subqueries to decompose complex queries

# ## Database
# 
# The database will be the customer relationship management (CRM) database, which has the following ERD.
# 
# ![Database-Schema.png](ERD.png)
# 
# ### Connect to the database
# 
# In the cell below we have provided the code to import both pandas and sqlite3 as well as define and create the connection to the database you will use. Also displayed is the schema and table names from the database. Use this information in conjunction with the ERD image above to assist in creating your SQL Queries.
# 
# Major Hint: Look for the shared columns across tables you need to 'join' together.

# In[ ]:


# CodeGrade step0
# Run this cell without changes

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)


# ## Part 1: Join and Filter

# ### Step 1
# 
# The company would like to let Boston employees go remote but need to know more information about who is working in that office. Return the first and last names and the job titles for all employees in Boston.

# In[12]:


# CodeGrade step1
# Replace None with your code
df_boston = pd.read_sql(""" 
select 
firstName,
lastName,
jobTitle
from employees
""", conn)


# ### Step 2
# 
# Recent downsizing and employee attrition have caused some mixups in office tracking and the company is worried they are supporting a 'ghost' location. Are there any offices that have zero employees?

# In[13]:


# CodeGrade step2
# Replace None with your code
df_zero_emp = pd.read_sql(""" 
SELECT 
    o.officeCode,
    COUNT(e.employeeNumber) AS employee_count
FROM offices o
LEFT JOIN employees e USING (officeCode)
GROUP BY o.officeCode
HAVING COUNT(e.employeeNumber) = 0;
""", conn)


# ## Part 2: Type of Join

# ### Step 3
# 
# As a part of this larger analysis project the HR department is taking the time to audit employee records to make sure nothing is out of place and have asked you to produce a report of all employees. Return the employees first name and last name along with the city and state of the office that they work out of (if they have one). Include all employees and order them by their first name, then their last name.

# In[14]:


# CodeGrade step3
# Replace None with your code
df_employee =  pd.read_sql(""" 
select 
firstName,
lastName,
city,
state
from employees
left join offices
USING(officeCode)
order by firstName,lastName
""", conn)


# ### Step 4
# The customer management and sales rep team know that they have several 'customers' in the system that have not placed any orders. They want to reach out to these customers with updated product catalogs to try and get them to place initial orders. Return all of the customer's contact information (first name, last name, and phone number) as well as their sales rep's employee number for any customer that has not placed an order. Sort the results alphabetically based on the contact's last name
# 
# There are several approaches you could take here, including a left join and filtering on null values or using a subquery to filter out customers who do have orders. In total there are 24 customers who have not placed an order.

# In[15]:


# CodeGrade step4
# Replace None with your code
df_contacts = pd.read_sql(""" 
select 
contactFirstName,
contactLastName,
phone,
salesRepEmployeeNumber
from customers
left join orders
USING(customerNumber)
where customerNumber NOT IN 
  (select customerNumber from orders)
""", conn)


# ## Part 3: Built-in Function

# ### Step 5
# 
# The accounting team is auditing their figures and wants to make sure all customer payments are in alignment, they have asked you to produce a report of all the customer contacts (first and last names) along with details for each of the customers' payment amounts and date of payment. They have asked that these results be sorted in descending order by the payment amount.
# 
# Hint: A member of their team mentioned that they are not sure the 'amount' column is being stored as the right datatype so keep this in mind when sorting.

# In[16]:


# CodeGrade step5
# Replace None with your code
df_payment = pd.read_sql(""" 
select
contactFirstName,
contactLastName,
phone,
paymentDate,
CAST (amount as float) as amount
from customers
join payments
using (customerNumber)
order by amount desc
""", conn)


# ## Part 4: Joining and Grouping

# ### Step 6
# 
# The sales rep team has noticed several key team members that stand out as having trustworthy business relations with their customers, reflected by high credit limits indicating more potential for orders. The team wants you to identify these 4 individuals. Return the employee number, first name, last name, and number of customers for employees whose customers have an average credit limit over 90k. Sort by number of customers from high to low.

# In[17]:


# CodeGrade step6
# Replace None with your code
df_credit = pd.read_sql(""" 
select 
employeeNumber,
lastName,
firstName,
count(salesRepEmployeeNumber) as num_of_customers
from employees
 join customers
on employeeNumber = salesRepEmployeeNumber
group by employeeNumber,lastName,firstName
having AVG(creditLimit) > 90000
order by count(customerNumber) desc
LIMIT 4;
""", conn)


# ### Step 7
# 
# The product team is looking to create new model kits and wants to know which current products are selling the most in order to get an idea of what is popular. Return the product name and count the number of orders for each product as a column named 'numorders'. Also return a new column, 'totalunits', that sums up the total quantity of product sold (use the quantityOrdered column). Sort the results by the totalunits column, highest to lowest, to showcase the top selling products.

# In[18]:


# CodeGrade step7
# Replace None with your code
df_product_sold = pd.read_sql(""" 
select 
productName,
productCode,
Count(orderNumber) as numorders,
sum(quantityOrdered) as totalunits
from products
join orderdetails
using(productCode)
group by productName
order by totalunits desc
""", conn)


# ## Part 5: Multiple Joins

# ### Step 8
# 
# As a follow-up to the above question, the product team also wants to know how many different customers ordered each product to get an idea of market reach. Return the product name, code, and the total number of customers who have ordered each product, aliased as 'numpurchasers'. Sort the results by the highest  number of purchasers.
# 
# Hint: You might need to join more than 2 tables. Use DISTINCT to return unique/different values.

# In[20]:


# CodeGrade step8
# Replace None with your code
df_total_customers = pd.read_sql(""" 
select 
productName,
products.productCode,
Count (DISTINCT customers.customerNumber) as numpurchasers
from products
LEFT join orderdetails
ON products.productCode = orderdetails.productCode
LEFT JOIN orders
ON orderdetails.orderNumber=orders.orderNumber
LEFT join customers
ON orders.customerNumber = customers.customerNumber
group by productName,products.productCode
order by numpurchasers desc
""", conn)


# ### Step 9
# 
# The custom relations team is worried they are not staffing locations properly to account for customer volume. They want to know how many customers there are per office. Return the count as a column named 'n_customers'. Also return the office code and city.

# In[22]:


# CodeGrade step9
# Replace None with your code
df_customers = pd.read_sql("""
select 
count(customerNumber) as n_customers,
employees.officeCode,
offices.city
from customers
join employees
on customers.salesRepEmployeeNumber = employees.employeeNumber
join offices
on employees.officeCode = offices.officeCode
group by offices.officeCode,offices.city
""", conn)


# ## Part 6: Subquery

# ### Step 10
# 
# Having looked at the results from above, the product team is curious to dig into the underperforming products. They want to ask members of the team who have sold these products about what kind of messaging was successful in getting a customer to buy these specific products. Using a subquery or common table expression (CTE), select the employee number, first name, last name, city of the office, and the office code for employees who sold products that have been ordered by fewer than 20 customers. **Sort the results alphabetically by last name.**
# 
# Hint: Start with the subquery, find all the products that have been ordered by 19 or less customers, consider adapting one of your previous queries.

# In[24]:


# CodeGrade step10
# Replace None with your code
df_under_20 = pd.read_sql(""" 
WITH employee_customer_counts AS (
    SELECT 
        e.employeeNumber,
        COUNT(DISTINCT c.customerNumber) AS num_customers
    FROM employees e
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber
    HAVING COUNT(DISTINCT c.customerNumber) < 20
)

SELECT 
    e.employeeNumber,
    e.firstName,
    e.lastName,
    o.city,
    e.officeCode
FROM employees e
JOIN offices o
    ON e.officeCode = o.officeCode
JOIN employee_customer_counts ecc
    ON e.employeeNumber = ecc.employeeNumber
ORDER BY 
    e.lastName ASC;

""", conn)


# ### Close the connection

# In[25]:


# Run this cell without changes

conn.close()


# In[ ]:




