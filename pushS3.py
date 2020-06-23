import boto3

s3 = boto3.client('s3')
s3.upload_file('output6.csv', 'adx-results', 'output6.csv')