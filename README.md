# Lambda pipeline example

## Overview

This is an example lambda "application" used for testing a lambda CI/CD pipeline.

The application is managed with AWS SAM (Serverless Application Model) and uses
AWS CodeBuild to build a deployment package.

### Layout

```
├── Makefile
├── buildspec.yml               - Used by CodeBuild to build and package the project for deployment
├── requirements.txt            - Third party Python libraries to install
├── src                         - Source code of the project
│   ├── hello.py                - The actual 'application'
│   └── pre_traffic_hook.py     - Hook used by CodeDeploy to verify the function is working after deployment
├── template.yaml               - SAM template
└── tests
    └── integration
        └── hello_test.py       - Example local integration test which uses pre traffic hook for validation
```

## Deployment

This application is deployed to AWS automatically on each commit to `master`.

CodePipeline will check it out from GitHub and run a CodeBuild task to build
and package the application as defined in `buildspec.yml`.  CodeBuild will
upload the artifact zip file to S3 and encrypt it with KMS.

A series of tests is triggered such as security scan or unit tests.  Those
run in parallel and are executed with AWS CodeBuild.

If tests pass, the application is deployed with CloudFormation (using
the SAM template) to a test account.  CodeDeploy will validate the
deployment using validation hooks.  If validation passes it will
update the function alias and direct new requests to the updated function.

Canary deployments are also possible.  See [Safe Lambda deployments](https://awslabs.github.io/serverless-application-model/safe_lambda_deployments.html) for details.

Manual approval is required to deploy to a production account.  Once approved
the same CloudFomation + CodeDeploy deployment/verification takes place as with
the test deployment.

## Testing verification hooks locally

NOTE:  This requires docker and sam-cli to be installed on your workstation.

It's possible to test verification hooks as used by CodeDeploy locally:

```
make integration_test_local
```

Under the hood this will:
 * build the application (creates a `build/` directory)
 * start local lambda endpoint
 * deploy the functions locally
 * Run pytest against tests/integration directory

The integration test in this example invokes the pre traffic hook function
which in turn does the actual validation of the application function (by doing
regex match on the output) and passes back the results.
