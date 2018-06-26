import boto3


def lambda_handler(event, context):
    firehose = boto3.client('firehose')
    firehose.put_record(
        DeliveryStreamName='firehose',
        Record={
            'Data': b'{"user_id": "a", "event": "AAA"}\n'
        }
    )
    firehose.put_record(
        DeliveryStreamName='firehose',
        Record={
            'Data': b'{"user_id": "b", "event": "BBB"}\n'
        }
    )
    firehose.put_record(
        DeliveryStreamName='firehose',
        Record={
            'Data': b'{"user_id": "c", "event": "CCC"}\n'
        }
    )
