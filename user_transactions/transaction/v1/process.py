
from user_transactions.models.v1.transaction import ExtractRequest
from user_transactions.transaction.v1.db import insert_transactions
from user_transactions.transaction.v1.balance import AccountBalance
from functools import reduce
import pandas as pd

async def generate_report(extract_data: ExtractRequest):
    
    df = pd.read_csv(f"./user_transactions/storage/account_{extract_data.account}.csv")
    
    
    df["date"] = df["date"].apply(lambda date: f"{extract_data.year}/{date}")
    df["date"] = pd.to_datetime(df['date'],format='ISO8601')
    
    
    await insert_transactions(iter(df.to_dict(orient="records")), len(df))
    
    df = df[df.date.dt.year == extract_data.year]
    
    
    # Get number of transactions grouped by month
    transactions = df.groupby(df.date.dt.month).agg(transactions_count=('value', 'count')).reset_index().rename({"date": "month"}, axis=1)
    
    
    # Get credit data by month
    df_credit = df[df["value"] > 0]
    average_credit = df_credit.agg(avg_credit=('value', 'mean'))
    total_credit_per_name = (df_credit.groupby(df.name)
                             .agg(total=("value", "sum"))
                             .sort_values(by=["total"], ascending=False)
                             .reset_index()
                             .rename({"date": "month"}, axis=1))
    
    # Get debit data by month
    df_debit = df[df["value"] < 0]
    df_debit.loc[:, "value"] = df_debit["value"].apply(lambda v: abs(v))
    average_debit = df_debit.agg(avg_debit=('value', 'mean'))

    total_debit_per_name = (df_debit.groupby(df.name)
                            .agg(total=("value", "sum"))
                            .sort_values(by=["total"], ascending=False)
                            .reset_index()
                            .rename({"date": "month"}, axis=1))
    
    
    summary = AccountBalance(account=extract_data.account,
                             total_balance=float(df["value"].sum().round(2)),
                             avg_transactions=pd.concat([average_credit, average_debit]),
                             balance_per_month=transactions,
                             total_debit_per_name=total_debit_per_name,
                             total_credit_per_name=total_credit_per_name,
    )
    
    summary.send_report(extract_data.receiver_email)