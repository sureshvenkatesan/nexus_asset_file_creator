#!/bin/bash

# Check if USER_PASSWORD environment variable is set
if [ -z "$USER_PASSWORD" ]; then
  echo "Error: USER_PASSWORD environment variable is not set."
  exit 1
fi

# Accept command-line arguments for Nexus URL, Username, and Script Name
NEXUS_URL=$1
USERNAME=$2
SCRIPT_NAME=$3

# Validate input parameters
if [ -z "$NEXUS_URL" ] || [ -z "$USERNAME" ] || [ -z "$SCRIPT_NAME" ]; then
  echo "Usage: $0 <NEXUS_URL> <USERNAME> <SCRIPT_NAME>"
  exit 1
fi

# Trigger the script execution using Nexus REST API
curl -u "$USERNAME:$USER_PASSWORD" \
    -X POST "$NEXUS_URL/service/rest/v1/script/$SCRIPT_NAME/run" \
    -H "Content-Type: text/plain" \
    -d '{}'

# Check if the script executed successfully
if [ $? -eq 0 ]; then
    echo "Groovy script '$SCRIPT_NAME' executed successfully."
else
    echo "Failed to execute Groovy script '$SCRIPT_NAME'."
fi
