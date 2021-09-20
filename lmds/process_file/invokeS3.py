from copy import Error
from tools.tools_aws import download_s3, call_lambda
import os 
from aws_lambda_powertools import Logger
logger = Logger(service="invokeS3")
BUCKET_NAME = os.environ["BUCKET_NAME"]
ARN_STORI = os.environ["ARN_STORI"]


class handled_data():
    def __init__(self,bucket_name, file_name):
        self.bucket_name = bucket_name
        self.file_name = file_name
        
    
    def process_csv(self,):
        try:
            logger.info("Starting to process the csv")
            datas = download_s3(self.bucket_name,self.file_name)
            underscore,point  = self.file_name.find("_"), self.file_name.find(".")
            user_name, last_name= self.file_name[:underscore], self.file_name[underscore+1:point:]
            body_dict = {"body":{"user_name":user_name,"lasts_name":last_name,"Id":[], "Date":[], "Transaction":[]} }
            for i, row in enumerate(datas.itertuples()):
                body_dict["body"]["Id"].append(row.Id)
                body_dict["body"]["Date"].append(row.Date)
                body_dict["body"]["Transaction"].append(row.Transaction)
            
            return body_dict

        except Exception as Error:
            logger.error("Something went wrongs trying to execute process_csv: {}".format(Error))
    

@logger.inject_lambda_context
def start(event, context):
    try:
        #event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-2', 'eventTime': '2021-09-19T22:56:54.516Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDARDCIIIDZWDH75OJQ2'}, 'requestParameters': {'sourceIPAddress': '187.194.108.182'}, 'responseElements': {'x-amz-request-id': 'QH4GFFJCD54JTQ8P', 'x-amz-id-2': 'ZWBKDMPxYf4pefmTEzTIfzUEpmhLHnXoMIAH9kC5Rt7OsCAxbHltjT069X9MT3vmyyBRR3N1byi5QWKJB/PsASy1qovzZh6G'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': 'dev-LMD_invokeS3-68a737133cefb25bff959852b8f04754', 'bucket': {'name': 'storidata', 'ownerIdentity': {'principalId': 'A3NO0909E13PA0'}, 'arn': 'arn:aws:s3:::storidata'}, 'object': {'key': 'test_1.csv', 'size': 73, 'eTag': 'ba2a38101febc2fce18d687ee4a2bd82', 'sequencer': '006147C03C9337487C'}}}]}
        
        logger.info("The event : {}".format(event))
        file_name= event["Records"][0]["s3"]["object"]["key"]
        logger.info("The file name of the event is : {}".format(file_name))
        process_data = handled_data(BUCKET_NAME, file_name)
        process_data = process_data.process_csv()

        call_lambda(ARN_STORI,process_data )
    
    except Exception as Error:
        logger.error("Error as: {}".format(Error))
