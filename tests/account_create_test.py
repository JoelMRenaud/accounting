import sqlite3
import sys

#Collecting input 

print("Give account name:")
name = input()

print("What is the account number:")
num = int(input())

print("What type of account is it (asset, liability, oe, income, expense):")
type = input()

#Connecting to db

con = sqlite3.connect("databases/company1.db")
cur = con.cursor()

res = cur.execute("SELECT * FROM accounts ORDER BY account_number")
accounts = res.fetchall()

#Checking input is viable

types = ["asset", "liability", "oe", "income", "expense"]
if type not in types:
    print("Not in types")
    sys.exit(1)

for i in range(len(accounts)):
    if num == int(accounts[i][0]):
        print("Number already used")
        sys.exit(2)
    if name == accounts[i][1]:
        print("Name already used")
        sys.exit(3)

#Updating
cur.execute("INSERT INTO accounts(account_number, name, type, value) VALUES (?,?,?,0)", (num,name,type,))
con.commit()
con.close()