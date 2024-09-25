import pandas as pd
import os, calendar

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


# Environment vars

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PASSWD = os.getenv("SMTP_PASSWD")

class AccountBalance:
    account: str
    total_balance: float
    balance_per_month: pd.DataFrame 
    avg_transactions: pd.DataFrame
    total_debit_per_name: pd.DataFrame 
    total_credit_per_name: pd.DataFrame 
    
    
    def __init__(self, account: str, total_balance: float, balance_per_month: pd.DataFrame, avg_transactions: pd.DataFrame, total_debit_per_name: pd.DataFrame, total_credit_per_name: pd.DataFrame):
        self.account = account
        self.total_balance = total_balance
        self.balance_per_month = balance_per_month
        self.avg_transactions = avg_transactions
        self.total_debit_per_name=total_debit_per_name,
        self.total_credit_per_name=total_credit_per_name,
        
        if type(self.total_debit_per_name) == tuple:
            self.total_debit_per_name = self.total_debit_per_name[0]
            
        if type(self.total_credit_per_name) == tuple:
            self.total_credit_per_name = self.total_credit_per_name[0]
        
        
    def send_report(self, receiver_email):
        

        # Define the email details
        
        basePath = str(os.path.abspath('.'))
        # Load the HTML content from a file
        with open(f"{basePath}/user_transactions/storage/email/template.html", 'r') as file:
            html_content = file.read()

        html_content = html_content.replace("[account_number]", self.account)
        html_content = html_content.replace("[total_balance]", str(self.total_balance))
        
        # Replace transactions in month
        
        month_transactions = ""
        for _, v in  self.balance_per_month.iterrows():
            
            template_month_transaction = '<p><span class="label">Transactions in {month}:</span> {value}</p><br>'.format(
                month=calendar.month_name[int(v.month)],
                value=v.transactions_count,
            )
            
            if month_transactions == "":
                month_transactions = template_month_transaction
                continue
            
            month_transactions += template_month_transaction
        
        html_content = html_content.replace("[month_transactions]", month_transactions)
        # Replace debit and credit average
        try:
            
            avg_debit = round(self.avg_transactions.loc["avg_debit"].value, 2)
            html_content = html_content.replace("[average_debit_amount]", str(avg_debit))
        
        except KeyError:
            html_content = html_content.replace("[average_debit_amount]", "-")
        
        try:
            
            avg_credit = round(self.avg_transactions.loc["avg_credit"].value, 2)
            html_content = html_content.replace("[average_credit_amount]", str(avg_credit))
        
        except KeyError:
            html_content = html_content.replace("[average_credit_amount]", "-")
            
            
        # Replace names of top debit and credit transactions
        
        top_debit = get_top_transactions(self.total_debit_per_name.head(3), "debit")
        top_credit = get_top_transactions(self.total_credit_per_name.head(3), "credit")
        
        
        html_content = html_content.replace("[top_debit_transactions]", top_debit)
        html_content = html_content.replace("[top_credit_transactions]", top_credit)

        sender_email = "reports@demomailtrap.com"
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your account report is now avalaible"
        message["From"] = sender_email
        message["To"] = receiver_email

        message.attach(MIMEText(html_content, "html"))
        
        
        image = MIMEImage(open(f"{basePath}/user_transactions/storage/email/logo.png", "rb").read())
        image.add_header('Content-ID', 'company_image')
        message.attach(image)
        
        with smtplib.SMTP(SMTP_HOST, 587) as server:
            server.starttls()
            server.login("api", SMTP_PASSWD)
            server.sendmail(sender_email, receiver_email, message.as_string())
            


def get_top_transactions(top_df: pd.DataFrame, tx_type: str) -> str:
    
    top_debit = ""
    multiplier = 1
    
    if tx_type == "debit":
        multiplier = -1
    
    for _, v in top_df.iterrows():
            
        if top_debit == "":
            top_debit = f"{v.loc['name']}:{round(multiplier * v.loc['total'], 2)} "
            continue
        
        top_debit += f"{v.loc['name']}:{round(multiplier * v.loc['total'], 2)} "
    
    return top_debit