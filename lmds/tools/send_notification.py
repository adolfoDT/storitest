#!/usr/bin/python3
# -*- encoding:utf-8 -*-
from logging import log
from time import process_time
from aws_lambda_powertools import Logger
logger = Logger(service="send_notification")
from tools.tools_sql import general_records
from tools.tools_aws import send_email
import os
import datetime
from itertools import groupby

HOST = os.environ["SQL_HOST"]
USER = os.environ["SQL_USER"]
PASSWORD = os.environ["SQL_PASSWORD"]

class Data:
    def __init__(self,user_name, last_name, ids, dates, transactions):
        self.username = user_name
        self.last_name = last_name
        self.ids = ids
        self.date = dates
        self.transactions = transactions
        self.query = general_records(HOST,USER,PASSWORD)
        self.total_balancer = sum(self.transactions)
        logger.info("The total balancer is : {}".format(self.total_balancer))
        self.query_user()

    def query_user(self,):
        try:
            logger.info("Query to user...")
            direction = "dbo.user_col where name = '{}' and last_name = '{}'".format(self.username, self.last_name)
            result_query =self.query.general_query("*", direction)
            if len(result_query) == 0:
                logger.info("Inserting user to the database")
                self.query.insert_query("dbo.user_col", "name, last_name, total_account", "'{}','{}',{}".format(self.username,self.last_name,self.total_balancer ))
            #TODO if the user doesn´t exist we add to the table
        except Exception as Error:
            logger.error("Something wents wrong trying to got the user: {}".format(Error))

#credit charges cames with +
#debit charges cames with -
class User_account(Data):
    def __init__(self, user_name, last_name, ids, dates, transactions):
        super().__init__(user_name, last_name, ids, dates, transactions)
         #credit are indicated with a plus ">"
         #debit are indicated by a minus "<""
        
        self.send_account_state()
     


    def process_data(self,):
        try:
            logger.info("Passing numbers dates to string dates")
            current_year = datetime.date.today().year
            dates_string = list()        
            for x in range(len(self.date)):
                index = self.date[x].find("/")
                day, month = int(self.date[x][index+1:]), int(self.date[x][:index])
                x = datetime.datetime(current_year, month, day)
                final_month='{0:%B}'.format(x)
                dates_string.append(final_month)
                
            #i don´t care about the sort of the data because i send data in order:
            # so my tuples will be in order
            create_tuple = list(zip(dates_string,self.transactions ))
            print("Create tuple : {}".format(create_tuple))
            return create_tuple

        except Exception as error:
            logger.error("Error in process_dates function : {}".format(error))
    
    def transactions_per_month(self,):
        try:
            logger.info("Getting transaction per month")
            group_transactions = self.process_data()

            new_list = list()
            for key, group in groupby(group_transactions, lambda x: x[0]):
                new_list.append(list(group))
            #sample list
            #[[('July', 60.5), ('July', -10.3)], [('August', -20.46)], [('December', 11.83)]]
           
            numbers_transactions = [ {"month": x[0][0], "total": str(len(x)) } for x in new_list ]

            #Output = numbers_transactions :[{'month': 'July', 'total': '2'}, {'month': 'August', 'total': '1'}, {'month': 'December', 'total': '1'}]
            
            logger.info("Transactions per month : {}".format(numbers_transactions))

            return numbers_transactions


        except Exception as Error:
            logger.error("Error in function transactions_per_month: {}".format(Error))

    def average_debit_credit(self):
        try:
            logger.info("Getting average of debit and credit")
            group_transactions = self.process_data()

            debit = [v for k, v in group_transactions if v < 0]

            credit = [v for k, v in group_transactions if v > 0]

            logger.info("List credit: {}, List Debit: {}".format(credit, debit))
            
            # the avegare is equal to the total between the numbers of elemnts
            average_debit = sum(debit)/len(debit)
            average_credit = sum(credit)/len(credit)

            return average_debit,average_credit

        except Exception as Error:
            logger.error("Error in function average_debit_credit: {}".format(Error))

        
    
    def send_account_state(self,):
        try:
            logger.info("Sending account state")
            debit , credit = self.average_debit_credit()
            column_values = "total_account = {}, credit_average = {}, debit_average = {}".format(self.total_balancer , credit, debit)
            self.query.update_query("dbo.user_col", column_values, "name = '{}' and last_name = '{}'".format(self.username, self.last_name))

            complete_name = self.username + " " + self.last_name

            numbers_transactions = self.transactions_per_month()

            send_email(self.total_balancer, numbers_transactions, debit, credit, complete_name)

        #Before send the email, we will insert the data to the database on Microsoft SQL

        except Exception as Error:
            logger.warning("Error while trying to send account state {}".format(Error))



        

            

        




        

        
