import tkinter as tk
from scripts.trial import trial_excel
from scripts.transaction import transactions
import sqlite3

#Connecting to server
con = sqlite3.connect("databases/company1.db")
cur = con.cursor()
res = cur.execute("SELECT * FROM accounts ORDER BY account_number")
accounts = res.fetchall()
accountNames = []
for i in range(len(accounts)):
    accountNames.append(accounts[i][1])






class home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Home page")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Export data to excel",
                           command=lambda: controller.show_frame(excel))
        button1.pack()

        button2 = tk.Button(self, text="Make a transaction",
                           command=lambda: controller.show_frame(transaction))
        button2.pack()

class excel(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Make spreadsheets")
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Make a trial balance", command=lambda: self.trial())
        button1.pack()

        button2 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(home))
        button2.pack()

    def trial(self):
        trial_excel(con=con)


class transaction(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.debits = 1
        self.credits = 1

        label = tk.Label(self, text="Make a Transaction")
        label.grid(row=0, column=2)
        add_debit = tk.Button(self, text="Add debit", command=lambda: self.increase_debit())
        add_debit.grid(row=1, column=1,pady=15)
        add_credit = tk.Button(self, text="Add credit", command=lambda: self.increase_credit())
        add_credit.grid(row=1, column=3,pady=15)

        self.debit_labels = []  # To store references to debit labels
        self.credit_labels = []  # To store references to credit labels
        self.debit_accounts = []  # To store references to debit accounts
        self.credit_accounts = []  # To store references to debit accounts
        self.debit_amounts = []  # To store references to debit amounts
        self.credit_amounts = []  # To store references to debit amounts

        self.update_labels()  # Initialize labels

        button = tk.Button(self, text="Submit",
                           command=lambda: self.submit())
        button.grid(row=1000, column=2, padx=20,pady=30)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame(home))
        button.grid(row=1001, column=2, padx=20)

    def submit(self):
        debit_accounts = [var.get() for var in self.debit_accounts]
        credit_accounts = [var.get() for var in self.credit_accounts]
        debit_values = [int(var.get()) for var in self.debit_amounts]
        credit_values = [int(var.get()) for var in self.credit_amounts]
        transactions(debitAccounts=debit_accounts,debits=debit_values,creditAccounts=credit_accounts,credits=credit_values, con=con)
        
        

    def update_labels(self):
        # Clear existing labels
        for widget in self.debit_labels:
            widget.destroy()
        self.debit_labels.clear()
        self.debit_accounts.clear()
        self.debit_amounts.clear()

        for i in range(self.debits):
            label = tk.Label(self, text="Debit {}".format(i + 1))
            label.grid(row=i * 3 + 2, column=1, pady=15)
            self.debit_labels.append(label)

            label = label = tk.Label(self, text="Amount")
            label.grid(row=i * 3 + 3, column=0, pady=15)
            self.debit_labels.append(label)

            clicked = tk.StringVar()
            drop = tk.OptionMenu(self, clicked, *accountNames)
            drop.grid(row=i * 3 + 3, column=1, pady=15)
            self.debit_labels.append(drop)
            self.debit_accounts.append(clicked)

            label = label = tk.Label(self, text="Account")
            label.grid(row=i * 3 + 4, column=0, pady=15)
            self.debit_labels.append(label)

            entry = tk.StringVar()
            input = tk.Entry(self,textvariable= entry)
            input.grid(row=i * 3 + 4, column=1, pady=15)
            self.debit_labels.append(input)
            self.debit_amounts.append(entry)

        # Clear existing labels
        for label in self.credit_labels:
            label.destroy()
        self.credit_labels.clear()
        self.credit_accounts.clear()
        self.credit_amounts.clear()
        
        for i in range(self.credits):
            label = tk.Label(self, text="Credit {}".format(i + 1))
            label.grid(row=i * 3 + 2, column=3, pady=15)
            self.credit_labels.append(label)

            label = label = tk.Label(self, text="Amount")
            label.grid(row=i * 3 + 3, column=2, pady=15)
            self.credit_labels.append(label)

            clicked = tk.StringVar()
            drop = tk.OptionMenu(self, clicked, *accountNames)
            drop.grid(row=i * 3 + 3, column=3, pady=15)
            self.credit_labels.append(drop)
            self.credit_accounts.append(clicked)

            label = label = tk.Label(self, text="Account")
            label.grid(row=i * 3 + 4, column=2, pady=15)
            self.credit_labels.append(label)

            entry = tk.StringVar()
            input = tk.Entry(self,textvariable= entry)
            input.grid(row=i * 3 + 4, column=3, pady=15)
            self.credit_labels.append(input)
            self.credit_amounts.append(entry)

    def increase_debit(self):
        self.debits += 1
        self.update_labels()

    def increase_credit(self):
        self.credits += 1
        self.update_labels()

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Ap CSA final project")

        # Set the initial window size
        self.geometry("500x500")

        # Bind the close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Initilize frames
        self.frames = {}
        for F in (home, excel, transaction):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(home)

    def show_frame(self, page_class):
        frame = self.frames[page_class.__name__]
        frame.tkraise()
    
    def on_closing(self):
        print("Application is closing...")
        con.commit()
        con.close()
        if self.winfo_exists():  # Check if the window still exists
            self.destroy()  # Close the Tkinter application

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()