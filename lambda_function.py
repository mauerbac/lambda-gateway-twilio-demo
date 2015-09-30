
import boto3
import os
import urllib2
import random

from boto3.session import Session
from twilio import twiml
from twilio.rest import TwilioRestClient
from boto3.dynamodb.conditions import Key, Attr

# create Twilio session
# 1) Add Twilio Keys
account_sid = "account id"
auth_token = "auth token"
client = TwilioRestClient(account_sid, auth_token)

# create an S3 & Dynamo session
s3 = boto3.resource('s3')
session = Session()
# 2) Add Dynamo Region and Table
dynamodb = boto3.resource('dynamodb', 'region')
table_users = dynamodb.Table('table-name')


def lambda_handler(event, context):

    body = event['body']
    fromNumber = event['fromNumber']
    image = event['image']
    numMedia = event['numMedia']

    # create response
    response = twiml.Response()
    response.ContentType = "application/xml"

    # check if we have their number
    response_dynamo = table_users.query(KeyConditionExpression=Key('fromNumber').eq(fromNumber))

    # a new user
    if response_dynamo['Count'] == 0:
        if len(message) == 0:
            response.message("Please send us an SMS with your name first!")
            return str(response)
        else:
            name = message.split(" ")
            table_users.put_item(Item={'fromNumber': fromNumber, 'name': name[0]})
            response.message("We've added {0} to the system! Now send us a selfie! ".format(name[0]))
            return str(response)
    else:
        name = response_dynamo['Items'][0]['name']

    if numMedia != '0':
        # get photo from s3
        pic_url = image
        twilio_pic = urllib2.Request(pic_url, headers={'User-Agent': "Magic Browser"})
        image_ = urllib2.urlopen(twilio_pic)
        # 3) Add S3 Bucket
        bucket = "s3-bucket"
        key = 'ingest-images/' + str(fromNumber.replace('+', '')) + '/' + str(random.getrandbits(50)) + '.png'
        resp_url = 'https://s3-us-west-2.amazonaws.com/{0}/{1}'.format(bucket, str(key))
        twilio_resp = 'Hi {0}, your S3 link: '.format(name) + 'https://s3-us-west-2.amazonaws.com/{0}/{1}'.format(bucket, str(key))
        # build meta data
        m_data = {'fromNumber': fromNumber, 'url': resp_url, 'name': name}
        s3.Bucket(bucket).put_object(Key=key, Body=image_.read(), ACL='public-read', ContentType='image/png', Metadata=m_data)
    else:
        response.message("No image found. :( ")
        twilio_resp = 'No image found'
    
    return twilio_resp
