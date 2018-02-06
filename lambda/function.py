from __future__ import print_function
import boto3

def lambda_handler(event, context):
    for record in event['Records']:
        s3 = record['s3']
        bucket = s3['bucket']['name']
        key = s3['object']['key'] 
        client=boto3.client('rekognition','us-west-2')
        response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':key}})
        print('Detected labels for ' + key)
        labels = []
        for label in response['Labels']:
            if label['Confidence'] > 60.0:
                labels.append(label['Name'])
            print (label['Name'] + ' : ' + str(label['Confidence']))
        dynamodb = boto3.client('dynamodb')
        response = dynamodb.put_item(TableName='SmartInstaImageLabels',Item={'PhotoId':{'S':key},'Labels':{'SS':labels}},ReturnConsumedCapacity='TOTAL')
        print("UpdateItem succeeded")
