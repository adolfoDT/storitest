#!/usr/bin/python3
# -*- encoding:utf-8 -*-

import os
import json
import logging
import boto3
import csv
from io import StringIO
import pandas as pd
from aws_lambda_powertools import Logger
logger = Logger(service="tools_aws")

__author__ = 'Adolfo Diaz Taracena'
__version__ = '1.0'

logger = logging.getLogger('tools_aws')


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
    
