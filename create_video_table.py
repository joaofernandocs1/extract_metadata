import boto3

# INPUT: 
# OUTPUT: 

def create_videos_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            #'dynamodb', endpoint_url="http://localhost:8000")
            'dynamodb', region_name="us-east-1") # trocar para sao paulo
 
    table = dynamodb.create_table(
        TableName='FlaggedVideos',
        KeySchema=[
            {'AttributeName': 'index_id',
            'KeyType': 'HASH'}, # Partition key
            {'AttributeName': 'duracao',
            'KeyType': 'RANGE' } # Sort key (realmente necessaria?)
        ],
        AttributeDefinitions=[
            {'AttributeName': 'index_id',
            'AttributeType': 'S'
            },
            {'AttributeName': 'duracao',
            'AttributeType': 'S'
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    return table
 
if __name__ == '__main__':

    videos_table = create_videos_table()
    print("Table status:", videos_table.table_status)
