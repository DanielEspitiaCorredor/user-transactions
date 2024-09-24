import pandas as pd
from random import randint, uniform, choice
from datetime import datetime, timedelta
import os


# transaction names
transactions = ["Nike Shoes", "Razer", "Apple", "Amazon", "Netflix", "Spotify", "Google Ads", "Uber", "Starbucks", "Paypal", 
                "Etsy", "Airbnb", "Target", "Walmart", "Zara", "H&M", "Adidas", "Ikea", "Lyft", "McDonald's"]

records = 100
account_id = "976133242399"

# Helper function to generate random dates
def random_date(start_month, end_month):
    
    start_date = datetime(2024, start_month, 1)
    end_date = datetime(2024, end_month, 31)
    random_days = randint(0, (end_date - start_date).days)
    
    return (start_date + timedelta(days=random_days)).strftime("%m/%d")



if __name__ == "__main__":
    
    filename = f"account_{account_id}.csv"
    file_path = f"{str(os.path.abspath('.'))}/user_transactions/storage"
    print(f"\n\nStart file generation {filename} in path {file_path} with {records} records")
    
    data = {
        "id": [i for i in range(records)],
        "date": [random_date(7, 8) for _ in range(records)],
        "name": [choice(transactions) for _ in range(records)],
        "value": [round(uniform(-1599, 1599), 2) for _ in range(records)]
    }

    # Creating DataFrame
    df = pd.DataFrame(data).to_csv(f"{file_path}/{filename}", index=False)
    
    print("File saved")