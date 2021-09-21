#!/usr/bin/python3
# -*- encoding:utf-8 -*-

import os
import json
import boto3
import csv
from io import StringIO
import pandas as pd
from aws_lambda_powertools import Logger
logger = Logger(service="tools_aws")

__author__ = 'Adolfo Diaz Taracena'
__version__ = '1.0'



def call_lambda(arn, event, type_invoke='Event',
                aws_access_key_id=None, aws_secret_access_key=None,
                region_name=None):
    """Call any lambda for testing.

    Use this function to test the behavior of the
    lambda function.
    Rememeber that you should have saved the configuration and
    the aws_access_key_id and the aws_secret_access_key in some
    configuration file in .aws path

    Args:
        arn (str): This is the Amazon resource Name (ARM) of your Lambda Function.
        event (dict): This is the param pased to the lambda usually a json object.
        type_invoke (str):
        aws_access_key_id (str):
        aws_secret_access_key (str):
        region_name (str):

    Returns:
        Anything that return the lambda function.
    """
    try:
        logger.info('Try create client lambda')
        
        if aws_access_key_id and aws_secret_access_key and region_name:
            client = boto3.client('lambda',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)
        elif aws_access_key_id and aws_secret_access_key:
            client = boto3.client('lambda',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
        else:
            client = boto3.client('lambda')
    except Exception as details:
        logger.error('Error to try make client(\'lambda\')\n'
                       'Details: {}'.format(details))
        return None
    # noinspection PyBroadException
    try:
  
        payload = json.dumps(event)
        logger.info("Invoking lambda function: {}".format(payload))
        result = client.invoke(FunctionName=arn,
                               InvocationType=type_invoke,
                               Payload=payload)
        
        

    except Exception as details:
        logger.error(f'Error to try invoke the lambda function.\n'
                     f'Detalles: {details}')
        return None
    logger.info('Function call_lambda finish successful.')
    return result['Payload'].read()


def download_s3(bucket, key):
                  
    try: 
        logger.info('Trying to create the instances for download the s3 file')
        s3_client = boto3.client('s3')
    except Exception as details:
        logger.error('Error went tried to connect to s3\nDetails: {}'.format(details))

    try:
        logger.info('The file was obtained successfully')
        response = s3_client.get_object(Bucket=bucket, Key=key)
        # data =json.loads(response["Body"].read())
        csv_string = response["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(csv_string))
        logger.info('The file was obtained successfully')
        return df
    except Exception as details:
        logger.error('Error went tried to get file: {}'.format(details))

def send_email(total_balancer, number_transactions, debit, credit, complete_name):
    logger.info("Sending email...")

   
    SENDER = "Storitest <diaz.taracenaAWS@gmail.com>"
    AWS_REGION = "us-east-2"
    SUBJECT = "Stori Account State of {}".format(complete_name)
    CHARSET = "UTF-8"
    emails = ["diaz.taracena94@gmail.com"]


    list_paras =["<p>Numbers of transactions in "+ each_one["month"] + " " + each_one["total"] + "</p>" for each_one in number_transactions ]

    paragraph = " ".join(list_paras)

    BODY_HTML = """<p> Total balancer {total_balancer}</p> {paragraph}
    <p>Average debit amount : {debit} </p>
    <p>Average credit amount : {credit} </p>
    """.format(total_balancer= total_balancer,paragraph = paragraph, debit=debit, credit=credit)

    # BODY_TEXT = """
    # These company: {companies_names} were inserted, to the Table = company_records_fra, please check
    # on the database is the record is not repeated
    # """

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    try:
        for each_email in emails:
            response = client.send_email(
                                Destination={
                                    'ToAddresses': [
                                        each_email,
                                    ],
                                },
                                Message={
                                    'Body': {
                                        'Html': {
                                            'Charset': CHARSET,
                                            'Data': BODY_HTML,
                                        },
                                        # 'Text': {
                                        #     'Charset': CHARSET,
                                        #     'Data': BODY_TEXT,
                                        # },
                                    },
                                    'Subject': {
                                        'Charset': CHARSET,
                                        'Data': SUBJECT,
                                    },
                                },
                                Source=SENDER,
                            )
    except Exception as error:
        logger.error("Errors were found in sending the notification, the deails are: {}.".format(error) )
        return False
    else:
        logger.warning("The notifications were sent!")
        return True
            
    
