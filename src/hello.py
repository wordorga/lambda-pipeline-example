import json
from cowpy import cow

def lambda_handler(event, context):
    moose = cow.Moose()
    msg   = moose.milk("hello")
    # msg   = moose.milk("helz")
    print "HELLO\n"
    return {
        "statusCode": 200,
        "headers": { "Content-Type": "text/plain"},
        "body": str(msg) + "\n",
    }
