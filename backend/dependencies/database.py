"""Crea las tablas.
"""
from typing import Annotated

from fastapi import Depends
from database.db_users import DBUsers
from database.db_payments import DBPayments
from database.db_deliveries import DBDeliveries
from database.db_products import DBProducts
from database.db_reviews import DBReviews
from sqlmodel import SQLModel
from dependencies.dbsession import engine

__database_users_instance = None
__database_payments_instance = None
__database_deliveries_instance = None
__database_products_instance = None
__database_reviews_instance = None


def init_db():

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    global __database_users_instance
    global __database_payments_instance
    global __database_deliveries_instance
    global __database_products_instance
    global __database_reviews_instance
    __database_users_instance = DBUsers()
    __database_payments_instance = DBPayments()
    __database_deliveries_instance = DBDeliveries()
    __database_products_instance = DBProducts()
    __database_reviews_instance = DBReviews() 
    

def get_db_users() -> DBUsers:
    global __database_users_instance


    if __database_users_instance is None:
        raise RuntimeError("Database Users instance not initialized.")
    
    return __database_users_instance

def get_db_payments() -> DBPayments:
    global __database_payments_instance


    if __database_payments_instance is None:
        raise RuntimeError("Database Payments instance not initialized.")
    
    return __database_payments_instance

def get_db_deliveries() -> DBUsers:
    global __database_deliveries_instance

    if __database_deliveries_instance is None:
        raise RuntimeError("Database Deliveries instance not initialized.")
    
    return __database_deliveries_instance

def get_db_products() -> DBProducts:
    global __database_products_instance


    if __database_products_instance is None:
        raise RuntimeError("Database Products instance not initialized.")
    
    return __database_products_instance

def get_db_reviews() -> DBReviews:
    global __database_reviews_instance

    if __database_reviews_instance is None:
        raise RuntimeError("Database Reviews instance not initialized.")
    
    return __database_reviews_instance

DBUsersDep = Annotated[DBUsers, Depends(get_db_users)]
DBPaymentsDep = Annotated[DBPayments, Depends(get_db_payments)]
DBDeliveries = Annotated[DBDeliveries, Depends(get_db_deliveries)]
DBProductsDep = Annotated[DBProducts, Depends(get_db_products)]
DBReviewsDep = Annotated[DBReviews, Depends(get_db_reviews)]