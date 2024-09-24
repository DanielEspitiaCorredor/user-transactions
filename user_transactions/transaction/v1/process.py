
from user_transactions.models.v1.transaction import ExtractRequest, AccountBalance
from user_transactions.transaction.v1.db import insert_transactions
from functools import reduce
import pandas as pd

def extract_and_insert_data(extract_data: ExtractRequest):
    # Total balance in the account, - OK
    # Number of transactions grouped by month - OK
    # Average credit by month - OK
    # average debit amounts by month - OK
    
    df = pd.read_csv(f"./user_transactions/storage/account_{extract_data.account}.csv")
    
    
    df["date"] = df["date"].apply(lambda date: f"{extract_data.year}/{date}")
    df["date"] = pd.to_datetime(df['date'],format='ISO8601')
    
    
    # insert_transactions(iter(df.to_dict(orient="records")), len(df))
    
    df = df[df.date.dt.year == extract_data.year]
    
    
    # Get number of transactions grouped by month
    transactions = df.groupby(df.date.dt.month).agg(TransactionsCount=('value', 'count')).reset_index().rename({"date": "month"}, axis=1)
    
    
    # Get credit data by month
    df_credit = df[df["value"] > 0]
    average_credit_by_month = (df_credit.groupby(df.date.dt.month)
                               .agg(avg_credit=('value', 'mean'))
                               .reset_index()
                               .rename({"date": "month"}, axis=1))
    total_credit_per_name = (df_credit.groupby(df.name)
                             .agg(total=("value", "sum"))
                             .sort_values(by=["total"], ascending=False)
                             .reset_index()
                             .rename({"date": "month"}, axis=1))
    
    # Get debit data by month
    df_debit = df[df["value"] < 0]
    df_debit.loc[:, "value"] = df_debit["value"].apply(lambda v: abs(v))
    average_debit_by_month = (df_debit.groupby(df.date.dt.month)
                              .agg(avg_debit=('value', 'mean'))
                              .reset_index()
                              .rename({"date": "month"}, axis=1))

    total_debit_per_name = (df_debit.groupby(df.name)
                            .agg(total=("value", "sum"))
                            .sort_values(by=["total"], ascending=False)
                            .reset_index()
                            .rename({"date": "month"}, axis=1))
    
    
    # summary = AccountBalance(total_balance=float(df["value"].sum().round(2)),
    #     balance_per_month=reduce(lambda left, right: pd.merge(left,right,on='month'), [transactions, average_credit_by_month, average_debit_by_month]),
    #     total_debit_per_name=total_debit_per_name,
    #     total_credit_per_name=total_credit_per_name,
    # )
    
    # summary.send_report()