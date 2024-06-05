import sqlite3
import sys
def transactions(debitAccounts, debits, creditAccounts, credits, con):
    cur = con.cursor()

    res = cur.execute("SELECT * FROM accounts ORDER BY account_number")
    accounts = res.fetchall()
    accountNames = []
    for i in range(len(accounts)):
        accountNames.append(accounts[i][1])


    if(sum(credits) == sum(debits)):

        #Make sure accounts exist
        for i in range(len(debits)):
            if (debitAccounts[i] not in accountNames):
                print("ACCOUNT " + debitAccounts[i] + " NOT FOUND")
                sys.exit(2)

        for i in range(len(credits)):
            if (creditAccounts[i] not in accountNames):
                print("ACCOUNT " + creditAccounts[i] + " NOT FOUND")
                sys.exit(2)

        # Updating sql database
        print("IT WORKED")
        for i in range(len(debits)):
            val = cur.execute("SELECT value FROM accounts WHERE name = ?", (debitAccounts[i],))
            val = int(''.join(map(str, val.fetchall()[0])))
            cur.execute("UPDATE accounts SET value = ? WHERE name = ?", (str(val + debits[i]), debitAccounts[i]))

        for i in range(len(credits)):
            val = cur.execute("SELECT value FROM accounts WHERE name = ?", (creditAccounts[i],))
            val = int(''.join(map(str, val.fetchall()[0])))
            cur.execute("UPDATE accounts SET value = ? WHERE name = ?", (str(val - credits[i]), creditAccounts[i]))

    else:
        print("DEBIT MUST EQUAL CREDIT")
        sys.exit(1)
    
    con.commit()
