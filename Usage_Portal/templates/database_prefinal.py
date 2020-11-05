# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 14:08:12 2020

@author: group e
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 23:00:08 2020

@author: group e
"""




import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE dispur_assam")

mydb1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dispur_assam"
)
mycursor1 = mydb1.cursor()

mycursor1.execute("CREATE TABLE user_type (Role_Id varchar(11) PRIMARY KEY ,Type_of_user VARCHAR(32) NOT NULL, Access_Level integer)")
mycursor1.execute("SHOW TABLES")

for x in mycursor1:
  print(x)
  

sql = "INSERT INTO user_type VALUES (%s, %s, %s)"
val = [
  ('CUST1', 'customer', 1),
  ('MNGR1', 'manager', 5),
  ('EMP1', 'employee', 2),
  ('HR1', 'HR', 3),
  ('ISM1','ISM', 4)
 ]
mycursor1.executemany(sql, val)

mydb1.commit()
mycursor1.execute("select * from user_type")
for i in mycursor1:
    print(i)
print(mycursor1.rowcount, "were inserted.")

mycursor2 = mydb1.cursor()

mycursor2.execute('''CREATE TABLE users (U_ID int(9) AUTO_INCREMENT primary key, User_Name varchar(255) NOT NULL, 
                    Address varchar(100) NOT NULL DEFAULT 'dispur',Email_ID varchar(320) NOT NULL, Contact_Number varchar(15) DEFAULT NULL,
                    Usr_Pwd varchar(32) NOT NULL, Usr_ConfirmPwd varchar(32) NOT NULL,isRegistered tinyint(1) NOT NULL DEFAULT 0, isActivated tinyint(1) NOT NULL DEFAULT 0, Role_id varchar(11), 
                    FOREIGN KEY (Role_id) REFERENCES user_type(Role_Id))''')
mycursor2.execute("SHOW TABLES")

for x in mycursor2:
  print(x)

sql1= "INSERT INTO users (User_Name, Email_ID, Contact_Number, Usr_Pwd, Usr_ConfirmPwd,Role_id) VALUES (%s, %s, %s, %s, %s, %s)"
val1 = [
  ('Shalini Bhatt', 'shalini@gmail.com', '8977754209' , 'flower123', 'flower123','CUST1'),
  ('Madhurima Handa', 'madhurima@gmail.com', '9762223098', 'test12345','test12345', 'CUST1'),
  ('Deepankar Vyas', 'deepankar@gmail.com', '9711098876', 'tcs12345','tcs12345', 'EMP1'),
  ('Priya Roy', 'priya@gmail.com', '7865410987', 'assam999','assam999', 'MNGR1'),
  ('user', 'user@gmail.com', '9887876309', 'password','password', 'CUST1'),
  ('user1','user1@gmail.com', '9866654365', 'password1','password1', 'CUST1'),
  ('admin', 'admin@gmail.com', '9876345212', 'administrator','administrator', 'ADMN1'),
  ('admin1', 'admin1@gmail.com', '9863211222', 'administrator1','administrator1', 'ADMN1')
]
mycursor2.executemany(sql1, val1)

mydb1.commit()
mycursor2.execute("select * from users")
for i in mycursor2:
    print(i)
print(mycursor2.rowcount, "were inserted.")





mycursor3 = mydb1.cursor()

mycursor3.execute("""CREATE TABLE plans (id int(11) auto_increment primary key,name varchar(255) NOT NULL,type varchar(5) 
                      NOT NULL,tariff decimal(6,2) NOT NULL,validity int NOT NULL,rental integer)""")
mycursor3.execute("CREATE TABLE adminlogin (id int(9) auto_increment primary key,uname VARCHAR(255), pas VARCHAR(255))")
mycursor3.execute("CREATE TABLE custlogin (id int(9)  auto_increment primary key,uname VARCHAR(255), pas VARCHAR(255))")
#mycursor3.execute("""CREATE TABLE address (userID int(9) NOT NULL,
#                  Lane_1 VARCHAR(1000) NOT NULL, Lane_2 VARCHAR(1000) DEFAULT NULL, 
#             city VARCHAR(50) NOT NULL, state VARCHAR(50) DEFAULT 'Assam', pincode VARCHAR(11) NOT NULL,
#            FOREIGN KEY (userID) REFERENCES users(u_ID))")

mycursor3.execute("SHOW TABLES")

for x in mycursor3:
  print(x)

sql = "INSERT INTO plans (name, type, tariff, validity, rental) VALUES (%s, %s, %s, %s, %s)"
val = [
  ('p1', 'type1', 1.2, 30, 500),
  ('p2', 'type2', 1.0, 30, 600),
  ('p3', 'type3', 0.8, 30, 700),
  ('p4', 'type4', 0.6, 30, 800),
  ('p5', 'type5', 0.4, 30, 900),
  ('p6', 'type6', 0.2, 30, 1000),
  ('p7', 'type7', 0.0, 30, 1100),
]

mycursor3.executemany(sql, val)

mydb1.commit()
mycursor3.execute("select * from plans")
for i in mycursor3:
    print(i)
print(mycursor3.rowcount, "were inserted.")


sql = "INSERT INTO adminlogin (uname, pas) VALUES (%s, %s)"
val = [
  ('admin','administrator'),
  ('admin1','administrator1'),
]

mycursor3.executemany(sql, val)

mydb1.commit()
mycursor3.execute("select * from adminlogin")
for i in mycursor3:
    print(i)
print(mycursor3.rowcount, "were inserted.")




sql = "INSERT INTO custlogin (uname, pas) VALUES (%s, %s)"
val = [
  ('user','password'),
  ('user1','password1'),
]

mycursor3.executemany(sql, val)

mydb1.commit()
mycursor3.execute("select * from custlogin")
for i in mycursor3:
    print(i)
print(mycursor3.rowcount, "were inserted.")


#sql = "INSERT INTO address (userID, Lane_1, Lane_2, city, state, pincode) VALUES (%s, %s, %s, %s, %s, %s)"
#val = [
#  (1, '202 Raghu Apartments, Collectrate Circle, Dispur, Assam,002016', 'NULL', 'Dispur', 'Assam', '002016'),
#  (2, '203 Raghu Apartments, Collectrate Circle, Dispur, Assam,002016','NULL', 'Dispur', 'Assam', '002016'),
#  (3, '204 Raghu Apartments, Collectrate Circle, Dispur, Assam,002016', 'NULL', 'Dispur', 'Assam', '002016'),
#  (4, '205 Raghu Apartments, Collectrate Circle, Dispur, Assam,002016', 'NULL', 'Dispur', 'Assam', '002016'),
#  (5, '206 Raghu Apartments, Collectrate Circle, Dispur, Assam,002016', 'NULL', 'Dispur', 'Assam', '002016'),
  
# ]

#mycursor3.executemany(sql, val)

#mydb1.commit()
#for i in mycursor3:
#    print(i)
#print(mycursor3.rowcount, "were inserted.")

mycursor4 = mydb1.cursor()

mycursor4.execute('''CREATE TABLE subscribes (U_ID int(9), Plan_ID int(11), 
                     Amount_Payable integer, Date_Of_Call date, Call_Duration integer, FOREIGN KEY (U_ID) 
                     REFERENCES users(U_ID), FOREIGN KEY (Plan_ID ) REFERENCES plans(id))''')
mycursor4.execute('''CREATE TABLE monthly_usage(U_Id int(9) , Plan_Id int(11) ,monthly_usage int (9), FOREIGN KEY (U_ID) 
                     REFERENCES users(U_ID), FOREIGN KEY (Plan_ID ) REFERENCES plans(id))''')
mycursor4.execute("SHOW TABLES")

for x in mycursor4:
  print(x)

sql1= "INSERT INTO subscribes (U_ID, Plan_ID, Amount_Payable, Date_Of_Call, Call_Duration) VALUES (%s, %s, %s, %s, %s)"
val1 = [
  (9, 1, 5000, '2020-10-31', 209),
  (10, 1, 5000, '2020-10-31', 98),
  (9, 2, 7000, '2020-10-31', 76),
  (10, 2, 7655, '2020-10-31', 87)
]
mycursor4.executemany(sql1, val1)


mydb1.commit()
mycursor4.execute("select * from subscribes")
for i in mycursor4:
    print(i)
print(mycursor4.rowcount, "were inserted.")


sql1= "INSERT INTO monthly_usage (U_ID, Plan_ID, monthly_usage) VALUES (%s, %s, %s)"
val1 = [
  (9, 1, 5000),
  (10, 1, 5000),
  (9, 2, 7000),
  (11, 2, 7655)
]
mycursor4.executemany(sql1, val1)


mydb1.commit()
mycursor4.execute("select * from monthly_usage")
for i in mycursor4:
    print(i)
print(mycursor4.rowcount, "were inserted.")


#mycursor5 = mydb1.cursor()

#mycursor5.execute('''CREATE TABLE customers (Cust_ID int(9) AUTO_INCREMENT Primary Key ,
#					Cust_Name varchar(255) NOT NULL, Address varchar(100) NOT NULL DEFAULT 'dispur',
#					Email_ID varchar(320) NOT NULL, Contact_Number varchar(15) DEFAULT NULL,
#                   Usr_Pwd varchar(32) NOT NULL, Usr_ConfirmPwd varchar(32) NOT NULL,
#                    isRegistered tinyint(1) NOT NULL DEFAULT 0, isActivated tinyint(1) NOT NULL DEFAULT 0) ''')
#mycursor5.execute("SHOW TABLES")

#for x in mycursor5:
#  print(x)

#sql1= "INSERT INTO customers (Cust_Name, Email_ID, Contact_Number, Usr_Pwd, Usr_ConfirmPwd) VALUES (%s, %s, %s, %s, %s)"
# val1 = [
#  ('Shalini Bhatt', 'shalini@gmail.com', '8977754209' , 'flower123', 'flower123'),
#  ('Madhurima Handa', 'madhurima@gmail.com', '9762223098', 'test12345','test12345'),
#  ('Deepankar Vyas', 'deepankar@gmail.com', '9711098876', 'tcs12345','tcs12345'),
#  ('Priya Roy', 'priya@gmail.com', '7865410987', 'assam999','assam999'),
#  ('user', 'user@gmail.com', '9887876309', 'password','password'),
#  ('user1','user1@gmail.com', '9866654365', 'password1','password1'),
#  ('admin', 'admin@gmail.com', '9876345212', 'administrator','administrator'),
#  ('admin1', 'admin1@gmail.com', '9863211222', 'administrator1','administrator1')
#]
#mycursor5.executemany(sql1, val1)

#mydb1.commit()
#mycursor5.execute("select * from customers")
#for i in mycursor5:
#    print(i)
#print(mycursor5.rowcount, "were inserted.")
