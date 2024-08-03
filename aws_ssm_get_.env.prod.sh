#!/bin/bash

# Define variables
ROLE_ARN="arn:aws:iam::014498632879:role/voicenger-role"
SESSION_NAME="AssumedRoleSession"
REGION="us-east-1"
PARAMETER_NAME="Prod"
OUTPUT_FILE=".env.prod"

# Assume the IAM role
echo "Assuming role: $ROLE_ARN"
ASSUME_ROLE_OUTPUT=$(aws sts assume-role --role-arn "$ROLE_ARN" --role-session-name "$SESSION_NAME" --region "$REGION")

# Check if role assumption was successful
if [ $? -ne 0 ]; then
    echo "Failed to assume role."
    exit 1
fi

# Extract temporary credentials
AWS_ACCESS_KEY_ID=$(echo $ASSUME_ROLE_OUTPUT | jq -r '.Credentials.AccessKeyId')
AWS_SECRET_ACCESS_KEY=$(echo $ASSUME_ROLE_OUTPUT | jq -r '.Credentials.SecretAccessKey')
AWS_SESSION_TOKEN=$(echo $ASSUME_ROLE_OUTPUT | jq -r '.Credentials.SessionToken')

# Export temporary credentials for the AWS CLI
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_SESSION_TOKEN

# Fetch the parameter value
echo "Fetching parameter: $PARAMETER_NAME"
aws ssm get-parameter --with-decryption --name "$PARAMETER_NAME" --region "$REGION" \
| jq -r '.Parameter.Value' \
| sed 's/\\n/\n/g' > "$OUTPUT_FILE"

# Check if the parameter fetch was successful
if [ $? -eq 0 ]; then
    echo "Parameters saved to $OUTPUT_FILE."
else
    echo "Failed to fetch parameters."
    exit 1
fi
