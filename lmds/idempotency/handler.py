import json
from aws_lambda_powertools.utilities.idempotency import (
    IdempotencyConfig, DynamoDBPersistenceLayer, idempotent
)
from aws_lambda_powertools import Logger



logger = Logger(service="Storitest")

persistence_layer = DynamoDBPersistenceLayer(table_name="IdempotencyTable")

# Treat everything under the "body" key
# in the event json object as our payload
config = IdempotencyConfig(event_key_jmespath="body")

@logger.inject_lambda_context
@idempotent(config=config, persistence_store=persistence_layer)
def start(event, context):
    try :
        logger.info("Starting the event...")
        logger.info("The events: {}".format(event))
        body = json.loads(event['body'])

        payment = create_subscription_payment(
            user=body['user'],
            product=body['product_id']
        )

        return {
            "payment_id": payment.id,
            "message": "success",
            "statusCode": 200
        }
    except Exception as Error:
        logger.error("Something wents wrong when trying to start the lambda:{}".format(Error))

