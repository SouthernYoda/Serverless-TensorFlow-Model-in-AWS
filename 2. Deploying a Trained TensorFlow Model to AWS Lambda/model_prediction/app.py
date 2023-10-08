import os
import json
import logging
import boto3
import base64

import numpy as np
import tensorflow as tf

from botocore.exceptions import ClientError

import zipfile
from io import BytesIO

temp_zip = '/tmp/model.zip'
model_contents = '/tmp/model_contents'

bucket = os.getenv('ModelBucket')
model_name = os.getenv('ModelName')
staging = os.getenv('StagingEnv')

log = logging.getLogger()
if staging == 'dev':
    log.setLevel(logging.DEBUG)
    tf.compat.v1.logging.set_verbosity(20)
elif staging == 'prod' or staging == 'preprod':
    log.setLevel(logging.INFO)
    tf.compat.v1.logging.set_verbosity(40)
else:
    raise Exception("Unknown staging env")

def lambda_handler(event, context):
    log.info("Invoking function")

    #############################################
    # Retrieve model from s3
    #############################################
    s3_client = boto3.client('s3', use_ssl=False) # create object for s3 service

    # download the zipped model from s3 and save it to a temporary location
    # the /tmp directoy location is ephemeral and only exists during the 
    # invocation of the function
    zip_obj = s3_client.download_file(Bucket=bucket, Key=model_name, Filename=temp_zip)
    log.debug(os.listdir('/tmp'))

    # unzip the model
    with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
        zip_ref.extractall('/tmp/model_contents')

    # create a string to store the location of the saved model
    model_folder = model_contents + '/' + os.listdir(model_contents)[0]
    log.debug(f"Model folder = {os.listdir(model_folder)}")

    #######################################################################
    # Prepare input
    #######################################################################

    # transform Embarked
    if event['Embarked'] == "C":
        event['Embarked_C'] = 1
        event['Embarked_Q'] = 0
        event['Embarked_S'] = 0
        event.pop("Embarked")
    elif event['Embarked'] == "Q":
        event['Embarked_C'] = 0
        event['Embarked_Q'] = 1
        event['Embarked_S'] = 0
        event.pop("Embarked")
    elif event['Embarked'] == "S":
        event['Embarked_C'] = 0
        event['Embarked_Q'] = 0
        event['Embarked_S'] = 1
        event.pop("Embarked")
    else:
        return(f"ERROR: input for Embarked with value {event['Embarked']} is invalid")

    # transform Sex
    if event["Sex"] == "male":
        event["Sex"] = 0
    elif event["Sex"] == "female":
        event["Sex"] = 1
    else:
        return(f"ERROR: input for Sex with value {event['Sex']} is invalid")
    
    #######################################################################
    # Model contents are the folder where the model files live
    #######################################################################

    #load the saved model
    model = tf.keras.models.load_model(model_folder)
    # this is useful when developing the lambda function and troubleshooting
    log.debug(model.summary())

    # this is also important to ensure the order of the features is consistent
    # when being fed to the model
    feature_keys = [
        "Pclass",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Fair",
        "Embarked_C",
        "Embarked_Q",
        "Embarked_S"
    ]

    # we are extracting just the feature values and transforming them into the proper format
    feature_values_list = []
    for key in feature_keys:
        feature_values_list.append(event[key])
    feature_values_for_predication = np.expand_dims(feature_values_list, axis=0)

    # create a predetion and save the result in a dictionary to be converted to a json string later.
    # for system to system communication it's best to use json
    model_prediction = {
        "input_features": event,
        "prediction": float(model.predict(x=feature_values_for_predication, verbose=0)[0])
    }

    return json.dumps(model_prediction)
