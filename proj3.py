#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/fhy9gs"
sqs = boto3.client('sqs', region_name='us-east-1')  

def delete_message(handle):
    try:
        Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_messages():
    messages = []
    try:
        # Receive messages from SQS queue.
        response = sqs.receive_message(
            QueueUrl=url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=10,  # Receive up to 10 messages at once
            MessageAttributeNames=[
                'All'
            ]
        )
        # Check if there are messages in the queue
        if "Messages" in response:
            for message in response['Messages']:
                order = message['MessageAttributes']['order']['StringValue']
                word = message['MessageAttributes']['word']['StringValue']
                handle = message['ReceiptHandle']
                messages.append({'order': order, 'word': word, 'ReceiptHandle': handle})
        else:
            print("No messages in the queue")
    except ClientError as e:
        print(e.response['Error']['Message'])
    return messages

def reassemble_phrase(messages):
    ordered_messages = sorted(messages, key=lambda x: int(x['order']))
    phrase = ' '.join(message['word'] for message in ordered_messages)
    return phrase

# Main function
def main():
    # Get messages from the queue
    messages = get_messages()

    if messages:
        print("Received messages:", messages)  # Print received messages for debugging
        # Reassemble the phrase
        phrase = reassemble_phrase(messages)
        print("Reassembled Phrase:", phrase)

        # Delete messages from the queue
        #for message in messages:
            #delete_message(message['ReceiptHandle'])

        # Write phrase to file
        with open('phrase.txt', 'w') as f:
            f.write(phrase + '\n')
            f.write("Partner: Quentin Shin")
            print("Phrase written to phrase.txt")
    else:
        print("No messages found in the queue.")

if __name__ == "__main__":
    main()

