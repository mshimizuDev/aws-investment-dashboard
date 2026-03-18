import boto3

s3 = boto3.client('s3')

def save_to_s3(bucket_name, key, data):

    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=data
    )