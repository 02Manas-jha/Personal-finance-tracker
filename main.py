import pandas as pd
import csv
from datetime import datetime
from data import get_amount,get_category,get_date,get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","category","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod #has access to other class methods
    def initialize_csv(cls):
        try: #here we are looking for our csv file if not found we make one
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS) #dataframe as the name suggests adds column rows to a csv file
            df.to_csv(cls.CSV_FILE,index = False)
    #now we add some information/entries in the csv
    @classmethod
    def add_entry(cls,date,amount,category,description):
        #use of csv writer to write into the file
        #we using dictionary and reason we using dict to write into the correct columns
        new_entry = {
            "date":date,
            "amount":amount,
            "category":category,
            "description":description
        }
        #we open the file in append mode, not overrinding and deleting anything 
        with open(cls.CSV_FILE,"a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            #csv writer takes a dictionary and write it into the csv file
            writer.writerow(new_entry)
        print("Entry added successfully")
    
    @classmethod
    #this method will give us all the transactions within a date range
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"],format=CSV.FORMAT) #this is done to ensure that date is going to be in the correct object.
        start_date = datetime.strptime(start_date,CSV.FORMAT)
        end_date = datetime.strptime(end_date,CSV.FORMAT)

        #creation of mask - something we can apply
        #To the different rows inside of a dataframe to see if we should select that row or not

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(f"Transcations from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ₹{total_income:.2f}")
            print(f"Total Expense: ₹{total_expense:.2f}")
            print(f"Net Savings: ₹{(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)


def plot_transaction(df):
    df.set_index('date',inplace=True)
    
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
        )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"],label="Income",color="g")
    plt.plot(expense_df.index,expense_df["amount"],label="Expense",color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and Expenses Over Time')
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new Transcation")
        print("2. View Transacrions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ") 
            df = CSV.get_transactions(start_date,end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transaction(df)
        elif choice == "3":
            print("Exiting..")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

if __name__ == "__main__":
    main()