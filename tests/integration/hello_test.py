import os
import boto3
import botocore
import json
import re

# Test the application by running the pre traffic hook function and checking
# it's status.  The same hook function is executed by CodeDeploy after
# deployment.

# Create Lambda SDK client to connect to local Lambda endpoint
lambda_client = boto3.client('lambda',
    region_name="eu-west-1",
    endpoint_url="http://127.0.0.1:3001",
    use_ssl=False,
    verify=False,
    config=botocore.client.Config(
        signature_version=botocore.UNSIGNED,
        read_timeout=100,
        retries={'max_attempts': 0},)
)

payload = {
    # '0000' id indicates local execution to the hook function.
    "DeploymentId": '0000',
    "LifecycleEventHookExecutionId": '0000',
    # Set CurrentVersion to the name of the function to be tested
    "CurrentVersion": 'hello'
}
payload = json.dumps(payload)

# Execute the hook function
response = lambda_client.invoke(
                FunctionName="CodeDeployHookHelloPreTraffic",
                Payload=payload
           )
response_json = json.loads(response['Payload'].read().decode('utf-8'))
status        = response_json['status']

def test_pre_traffic_hook():
    assert status == 'Succeeded'
