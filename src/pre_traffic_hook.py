import json
import boto3
import botocore
import re
import os

def lambda_handler(event, context):

    deployment_id = event['DeploymentId']
    lifecycle_event_hook_execution_id = event['LifecycleEventHookExecutionId']

    if deployment_id == '0000':
        local = True
        print 'Running locally'
        target_function = event['CurrentVersion']
    else:
        local = False
        target_function = os.environ['CurrentVersion']

    print 'Starting pre traffic validation hook for function %s', target_function

    if local:
        # Use the local lambda endpoint when testing locally
        lambda_client = boto3.client('lambda',
            region_name="eu-west-1",
            endpoint_url="http://host.docker.internal:3001",
            use_ssl=False,
            verify=False,
            config=botocore.client.Config(
                signature_version=botocore.UNSIGNED,
                read_timeout=100,
                retries={'max_attempts': 0},
            )
        )
    else:
        lambda_client = boto3.client('lambda')

    # Invoke the target function and test it's operation
    print 'Validating function'

    response      = lambda_client.invoke(FunctionName=target_function)
    response_json = json.loads(response['Payload'].read().decode('utf-8'))

    status = 'Failed'
    if re.search('hello', response_json['body']):
        status = 'Succeeded'

    print "Got status: %s" % status

    if local:
        # Return status which can be checked in local tests
        return {
            'status': status
        }
    else:
        # Notify CodeDeploy with status if running in AWS.
        print("Notifying CodeDeploy")
        cd_client = boto3.client('codedeploy')
        cd_response = cd_client.put_lifecycle_event_hook_execution_status(
            deploymentId=deployment_id,
            lifecycleEventHookExecutionId=lifecycle_event_hook_execution_id,
            status=status
            )
