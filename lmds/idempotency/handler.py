
import json
from logging import error
import logging
from aws_lambda_powertools.utilities.idempotency import (
    IdempotencyConfig, DynamoDBPersistenceLayer, idempotent
)
from aws_lambda_powertools import Logger

logger = Logger(service="tools_aws")

persistence_layer = DynamoDBPersistenceLayer(table_name="IdempotencyTable")


#TODO checar con la configuracion PARA LA IDEMPOTENTENCYnormal sin el event_key_jmespath, eso posiblemente funcione
#TODO crear notificacion con SES
#TODO en la base de datos solicitar el tipo de notificacion que se va a enviar
#TODO checar si la tabla de users de la base de datos tienen emails
#TODO al terminar de solicitar los cargos, actualizar la cantidad total disponible en base a la cuenta de credito y debito
#TODO puede que en produccion no funcione la persistencia del data layer de dinamaco checar eso
#TODO AL FINALIZAR EDITAR UN README DE TODOS LOS SERVICIOS QUE USO, COMO SE USARON, COMO PUEDEN INSTALAR EL SERVICIO Y CREAR UNAS CUENTAS PROVISIONALES EN AWS

# @idempotent(config=config, persistence_store=persistence_layer)
@idempotent(persistence_store=persistence_layer)
def start(event, context):
    try:
        data_type = type(event)
    
        logger.info("The event is : {}".format(event))
        logger.info("The data type is: {}".format(str(data_type)))
       

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
        logger.error("Something wents wrong: {}".format(Error))