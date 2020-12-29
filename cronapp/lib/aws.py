import boto3 
import json

from lib.config import LAMBDA_GET_FUNCTION

lambda_client = boto3.client('lambda', region_name='us-east-1')

def get_overrides():
    return \
        json.loads(
            json.loads(
                lambda_client.invoke(
                    FunctionName=LAMBDA_GET_FUNCTION
                )['Payload'].read().decode('utf-8')
            )
        )

def apply_overrides(new_rules, overrides):
    print(new_rules)
    print(overrides)

    overridden_rules = new_rules

    return overridden_rules
