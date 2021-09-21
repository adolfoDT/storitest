
import json
from aws_lambda_powertools.utilities.idempotency import (
    IdempotencyConfig, DynamoDBPersistenceLayer, idempotent
)
from aws_lambda_powertools import Logger
from tools.send_notification import User_account
logger = Logger(service="tools_aws")

persistence_layer = DynamoDBPersistenceLayer(table_name="IdempotencyTable")

# @idempotent(config=config, persistence_store=persistence_layer)
@idempotent(persistence_store=persistence_layer)
def start(event, context):
    try:
        data_type = type(event)
    
        logger.info("The event is : {}".format(event))
        logger.info("The data type is: {}".format(str(data_type)))

        user_name = event["body"]["user_name"]
        lasts_name = event["body"]["lasts_name"]
        Ids = event["body"]["Id"]
        Dates = event["body"]["Date"]
        Transaction = event["body"]["Transaction"]
       
        User_account(user_name,lasts_name, Ids,Dates, Transaction  )
        
        return {
            "message": "success",
            "statusCode": 200
        }
    except Exception as Error:
        logger.error("Something wents wrong: {}".format(Error))