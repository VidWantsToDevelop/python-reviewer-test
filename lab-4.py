import boto3

def syncTables(event, context):
    source_ddb = boto3.client('dynamodb', 'us-east-1')
    destination_ddb = boto3.client('dynamodb', 'us-west-2')
    paginator =
    sync_ddb_table(source_ddb, destination_ddb)

# Scan returns paginated results, so only partial data will be copied
def sync_ddb_table(source_ddb, destination_ddb):
    done = False
    start_key = None
    scan_kwargs = {}
    while not done:
      if start_key:
          scan_kwargs['ExclusiveStartKey'] = start_key
      response = source_ddb.scan(
          TableName="<FMI1>", **scan_kwargs
      )

      for item in response['Items']:
          destination_ddb.put_item(
              TableName="<FMI2>",
              Item=item
          )
      start_key = response.get("LastEvaluatedKey", None)
      done = start_key is None
