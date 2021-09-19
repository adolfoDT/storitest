#!/usr/bin/python3
# -*- encoding:utf-8 -*-

import os
import json
import logging
import boto3

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
        print('Try create client lambda.')
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
        print('Error to try make client(\'lambda\')\n'
                       'Details: {}'.format(details))
        return None
    # noinspection PyBroadException
    try:
        print(event)
        print("intentando.....")
        print("s3INVOKEEE")
        payload = json.dumps(event)
        print("datetime")
        print(payload)
        result = client.invoke(FunctionName=arn,
                               InvocationType=type_invoke,
                               Payload=payload)
        print("datetime")
        

    except Exception as details:
        print(f'Error to try invoke the lambda function.\n'
                     f'Detalles: {details}')
        return None
    print('Function call_lambda finish successful.')
    return result['Payload'].read()


def descarga_de_s3(bucket, nombre_archivo, carpeta_s3=None, path_save_file='/tmp/', nuevo_nombre=None,
                   aws_access_key_id=None, aws_secret_access_key=None,
                   region_name=None):
    try:
        print('Trying to create the instances for download the file.')
        if aws_access_key_id and aws_secret_access_key and region_name:
            s3 = boto3.resource('s3',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                region_name=region_name)
        elif aws_access_key_id and aws_secret_access_key:
            s3 = boto3.resource('s3',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
        else:
            s3 = boto3.resource('s3')
    except Exception as details:
        print('Error to try connect to s3\nDetails: {}'.format(details))
        return None

    if carpeta_s3 is None:
        path_s3_file = nombre_archivo
    else:
        path_s3_file = f'{carpeta_s3}/{nombre_archivo}'

    if nuevo_nombre is None:
        path_save_file = os.path.join(path_save_file, nombre_archivo)
    else:
        path_save_file = os.path.join(path_save_file, nuevo_nombre)
    try:
        s3.Bucket(bucket).download_file(path_s3_file, path_save_file)
    except Exception as details:
        print('Error while trying to download {} a {}\n'
                       'Error details: {}'.format(path_s3_file, path_save_file, details))
        raise ErrorDescargaS3(details)
    else:
        print('Successfull download.')
        return s3.Object(bucket, path_s3_file).metadata

class ErrorDescargaS3(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)


class ErrorCargaS3(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)