import google.cloud.logging
import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def setup_logging(log_level=LOG_LEVEL):
    if is_cloud_function():
        setup_cloud_function_logger()
    else:
        logging.basicConfig(level=log_level)

def is_cloud_function():
    K_SERVICE = os.getenv('K_SERVICE')
    return K_SERVICE != None

def setup_cloud_function_logger(log_level):
    google.cloud.logging.Client().setup_logging(log_level=log_level)
