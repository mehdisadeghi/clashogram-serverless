import os
import json

import boto3
import requests
import clashogram


dynamodb = boto3.resource('dynamodb')


class SimpleDynamoKVDB(object):
    """A dynamodb wrapper.

    Similar to https://github.com/python/cpython/blob/master/Lib/shelve.py
    """
    def __init__(self, tblname):
        self.table = dynamodb.Table(tblname)
        self.writeback = True  # Always writeback
        self.cache = {}

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.sync()

    def __contains__(self, key):
        try:
            return self[key] is not None
        except KeyError:
            return False

    def __getitem__(self, key):
        try:
            value = self.cache[key]
        except KeyError:
            response = self.table.get_item(Key={'warId': key})

            if 'Item' not in response:
                raise KeyError(key)

            value = json.loads(response['Item']['warDict'])
            if self.writeback:
                self.cache[key] = value

        return value

    def __setitem__(self, key, value):
        if self.writeback:
            self.cache[key] = value

        self.table.put_item(Item={'warId': key, 'warDict': json.dumps(value)})

    def __delitem__(self, key):
        self.table.delete_item(Key={'warId': key})
        try:
            del self.cache[key]
        except KeyError:
            pass

    def sync(self):
        if self.writeback and self.cache:
            self.writeback = False
            for key, entry in self.cache.items():
                self[key] = entry
            self.writeback = True
            self.cache = {}


def logger(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({'message': event})
    }


def caller(event, context):
    resp = requests.get(os.environ['URI'])
    return {
        'statusCode': 200,
        'body': json.dumps({'message': resp.content.decode('utf-8')})
    }


def main(event, context):
    # Do a single update and return.
    with SimpleDynamoKVDB(os.environ['WARLOG_TABLE']) as db:
        clashogram.serverless(
            db,
            os.environ['COC_API_TOKEN'],
            os.environ['COC_CLAN_TAG'],
            os.environ['TELEGRAM_BOT_TOKEN'],
            os.environ['TELEGRAM_CHANNEL'])

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


if __name__ == '__main__':
    main(None, None)
