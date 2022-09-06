import json
import urllib.parse
import boto3
import os

#Jenkins test deployment github-webhook/    

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print('buckent name is' + bucket)
    print('key name is' + key)
    try:
        sqs_queue_url = os.environ.get("sqs_queue_url")
        send_sqs_message(sqs_queue_url, bucket,key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
        
def send_sqs_message(sqs_queue_url, bucket,key):
    # Send the SQS message
    sqs_client = boto3.client('sqs')
    msg_body = {"bucket": bucket, "key": key}
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=json.dumps(msg_body))
        print(msg)
        print("msg pushed to sqs queue")
    except ClientError as e:
        print(e)
        return None
    return msg
