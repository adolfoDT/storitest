#!/usr/bin/python3
# -*- encoding:utf-8 -*-

import sys
import logging
import decimal
from pymssql import _mssql
from datetime import datetime, timedelta
from aws_lambda_powertools import Logger
logger = Logger(service="tools_sql")


__author__ = 'Adolfo Diaz Taracena'
__version__ = '1.0'

class SQLManagerConnections:
    def __init__(self, host, user, password):
        super(SQLManagerConnections, self).__init__()
        self.__host = host
        self.__user = user
        self.__password = password
        self.conexion = None
        self.__max_tries_for_close_conexions = 5
        self.__tries_for_close_conexions = 0
    def connect(self, database):
        try:
            logger.info('Connecting to the database: {}'.format(database))
            self.conexion = _mssql.connect(server=self.__host,
                                           user=self.__user,
                                           password=self.__password,
                                           database=database)
        except _mssql.MssqlDatabaseException as error:
            logger.error('Error while trying to connect to database.'
                                ' Error: {}'.format(error))
            sys.exit(1)
        else:
            logger.info('Connecting to the database:: {}'.format(database))

    def check_open_conexions(self):
        if self.__max_tries_for_close_conexions > self.__tries_for_close_conexions:
            if self.conexion.connected:
                logger.warning('The connection still open.'
                                      'Trying to close connection...')
                self.conexion.close()
                self.__tries_for_close_conexions += 1
                self.check_open_conexions()
            else:
                logger.info('There is not open connections.')
                self.__tries_for_close_conexions = 0
        else:
            logger.warning('It was not possible to close the connection after {} attempts'
                                  ' try to kill the connection from the system.'
                                  ''.format(self.__tries_for_close_conexions))
            self.__tries_for_close_conexions = 0

class general_records(SQLManagerConnections):
    def __init__(self, host, user, password):
        super(general_records, self).__init__(host, user, password)
 
    def __Ejecutar_qry(self, databse, qry):
        self.connect(databse)
        if not (self.conexion is None):
            # noinspection PyBroadException
            try:
                self.conexion.execute_query('{}'.format(qry))
            except Exception as details:
                logger.warning(f'Problems in the execution of the query\n'
                                      f'Details: {details}')
            resultado = self.__debug_query()
            self.conexion.close()
            self.check_open_conexions()
            return resultado
    def __debug_query(self):
        try:
            resultado = []
            for reg in self.conexion:
                registro = []
                for llave in list(reg.keys()):
                    if type(llave) is str:
                        if type(reg[llave]) is decimal.Decimal:
                            if not reg[llave].is_nan():
                                try:
                                    reg[llave] = int(reg[llave])
                                except ValueError:
                                    reg[llave] = float(reg[llave])
                        registro.append((llave, reg[llave]))
                resultado.append(dict(registro))
        except Exception as details:
            logger.error('Error trying to debug the query.\n'
                                'Details: {}'.format(details))
            self.check_open_conexions()
        else:
            logger.debug(resultado)
            return resultado
    def general_query(self,columns, direction):
        try:
            qry =""" 
            SELECT {columns} FROM {direction}
                
            """.format(columns= columns, direction = direction)
        except Exception as err:
            logger.warning(f"There was a problem building the query: {err}")
            return []
        resp = self.__Ejecutar_qry("framework",qry)
        print("response")
        print(resp)
        return resp

    def insert_query(self,table,columns, values):
        try:
            qry =""" 
            INSERT INTO  {table}(
                {columns} 
            ) VALUES ({values})
                
            """.format(table = table,columns= columns, values = values)
            logger.info("Inserting query: {}".format(qry))
        except Exception as err:
            logger.warning(f"There was a problem building the query: {err}")
            return []
        resp = self.__Ejecutar_qry("framework",qry)
        return resp

    def update_query(self,table,column_values, condition):
        try:
            qry =""" 
            UPDATE {table}
            SET {column_values}
            WHERE {condition}
                
            """.format(table = table,column_values= column_values, condition = condition)
            logger.info("Updating query: {}".format(qry))
        except Exception as err:
            logger.warning(f"There was a problem updating the query: {err}")
            return []
        resp = self.__Ejecutar_qry("framework",qry)
        return resp