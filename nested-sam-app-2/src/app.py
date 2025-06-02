import json
import boto3
import os
import logging
from urllib.parse import unquote_plus

# ロガーの設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    logger.info('Received event: %s', json.dumps(event))
    
    try:
        # イベントからバケット名とオブジェクトキーを取得
        source_bucket = event['detail']['bucket']['name']
        object_key = unquote_plus(event['detail']['object']['key'])
        
        logger.info('Source bucket: %s', source_bucket)
        logger.info('Object key: %s', object_key)
        
        # 環境変数から出力バケット名を取得
        dest_bucket = os.environ['OUTPUT_BUCKET_NAME']
        if not dest_bucket:
            raise ValueError("OUTPUT_BUCKET_NAME environment variable is not set")
        
        logger.info('Destination bucket: %s', dest_bucket)
        
        # S3からS3へのコピー操作
        copy_source = {
            'Bucket': source_bucket,
            'Key': object_key
        }
        
        s3_client.copy_object(
            CopySource=copy_source,
            Bucket=dest_bucket,
            Key=object_key
        )
        
        logger.info('Successfully copied %s from %s to %s', object_key, source_bucket, dest_bucket)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File copied successfully',
                'source': f'{source_bucket}/{object_key}',
                'destination': f'{dest_bucket}/{object_key}'
            })
        }
    
    except Exception as e:
        logger.error('Error: %s', str(e), exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error copying file',
                'error': str(e)
            })
        }
