import json
import pprint
import boto3
import os

dynamo = boto3.client('dynamodb')
table = 'pfsenseParentalControlConfig'

key_field = 'config_id'
key_type = 'S'
key_value = '0'

payload_field = 'payload'
payload_type = 'S'

def get_parental_control_config(event, context):
    response = \
        dynamo.get_item(
            TableName=table,
            Key={ key_field: { key_type: key_value } }
        )['Item'][payload_field][payload_type]

    return response

def set_parental_control_config(event, context):
    data = event

    item = {
        key_field: { key_type: key_value },
        payload_field: { payload_type: json.dumps(data) }
    }

    response = \
        dynamo.put_item(
            TableName=table,
            Item=item
        )
    
    return json.dumps(response)

if __name__ == '__main__':
    import sys
    _, f = sys.argv

    if f == 'get_parental_control_config':
        print(get_parental_control_config("", ""))
    
    if f == 'set_parental_control_config':
        print(set_parental_control_config("", ""))
