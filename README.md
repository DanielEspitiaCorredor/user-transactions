# user-transactions

Project used to process debit and credit transactions

# Components

The user_transactions project is a REST API developed using FastAPI, structured into several modules.

The first module is the authentication module, which provides two endpoints for user registration and login. Authentication is facilitated through JSON Web Tokens (JWT), which remain valid for one hour.

The second module, known as the transaction module, is responsible for processing CSV files, generating reports, and sending emails.

In this project you can find auxiliary modules, that include an middleware designed to handle and manage any errors that may occur during requests. In the scripts folder, you will find the script that generates data for the CSV file, you can use this script to generate new file if you needed. The file is created with the following columns: ID, date, transaction name, and value.

The models directory contains the data models used for requests and responses. The project save data of users and transactions using Object Document Mapper (ODM), and the data is stored in MongoDB.


The storage folder contains the CSV file used for the project, along with the email template created for communication purposes.

To send emails, the AccountBalance class is utilized, which integrates the relevant information into the HTML template and manages the email delivery process


# Prerequisites

- Docker
- Docker compose


# Get Started


For configure this project, please set the env file in the project path

![alt text](/user_transactions/storage/readme/setenv.png)


This project use a docker-compose file to launch two containers. The first is the fastapi application and the other is a mongo database.

```
docker compose up -d --build
```

After of this step, go to the http://127.0.0.1:8000/docs and it show all endpoints avalaible.

![alt text](/user_transactions/storage/readme/fastapi.png)

The first endpoint register an user in the users collections

![alt text](/user_transactions/storage/readme/mongo.png)

After this, log in executing the login endpoint. This will provide you a bearer token that you should configure in the Authorize header.


![alt text](/user_transactions/storage/readme/login.png)

Finally, when authentication is ok, you can execute the endpoint to generate report. This service process a file csv. you can set the following params

- account: generic value to associate transactions to an account 
- year: Used to complement dates in csv file. If the value is 2024, in the database the value is 2024/09/02
- receiver_email: email used to receive the balance


![alt text](/user_transactions/storage/readme/generate_report.png)


When you use this endpoint, you receive an email with the balance of your account

![alt text](/user_transactions/storage/readme/report.png)

# Generate data

To generate a new file with test data execute `make generate-csv`. This command creates a new file that you can use in this project