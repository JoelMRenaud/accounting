import sqlite3
import sys

con = sqlite3.connect("databases/company1.db")
cur = con.cursor()

res = cur.execute("SELECT * from accounts")
data = res.fetchall()

print("Make a transaction")

print("How many debits:")
debitCount = int(input())
debits = []
debitAccounts = []

for i in range(debitCount):

    print("Debit amount:")
    debits.append(int(input()))
    print("Debit account number:")
    debitAccounts.append(int(input()))


print("How many credits:")
creditCount = int(input())
credits = []
creditAccounts = []

for i in range(creditCount):

    print("Credit amount:")
    credits.append(int(input()))
    print("Credit account number:")
    creditAccounts.append(int(input()))


res = cur.execute("SELECT * FROM accounts ORDER BY account_number")
accounts = res.fetchall()
accountNums = []
for i in range(len(accounts)):
    accountNums.append(accounts[i][0])


if(sum(credits) == sum(debits)):

    #Make sure accounts exist
    for i in range(len(debits)):
        if (debitAccounts[i] not in accountNums):
            print("ACCOUNT " + str(debitAccounts[i]) + " NOT FOUND")
            sys.exit(2)

    for i in range(len(credits)):
        if (creditAccounts[i] not in accountNums):
            print("ACCOUNT " + str(creditAccounts[i]) + " NOT FOUND")
            sys.exit(2)

    # Updating sql database
    for i in range(len(debits)):
        val = cur.execute("SELECT value FROM accounts WHERE account_number = ?", (str(debitAccounts[i]),))
        val = int(''.join(map(str, val.fetchall()[0])))
        cur.execute("UPDATE accounts SET value = ? WHERE account_number = ?", (str(val + debits[i]), str(debitAccounts[i])))

    for i in range(len(credits)):
        val = cur.execute("SELECT value FROM accounts WHERE account_number = ?", (str(creditAccounts[i]),))
        val = int(''.join(map(str, val.fetchall()[0])))
        cur.execute("UPDATE accounts SET value = ? WHERE account_number = ?", (str(val - credits[i]), str(creditAccounts[i])))

else:
    print("ERROR: DEBIT MUST EQUAL CREDIT")
    sys.exit(1)

con.commit()
con.close()
