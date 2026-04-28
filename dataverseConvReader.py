"""
Dataverse Conversation Reader

This script connects to Microsoft Dataverse, fetches conversation transcripts
from the last N days, and extracts user reactions (like/dislike) with feedback.

Configuration is loaded from a .env file for security.
"""

import requests
import json
import os
import sys
from msal import ConfidentialClientApplication
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import reactionreader

# Load environment variables from .env file
load_dotenv()

# -------- CONFIGURATION ----------
# Load required configuration from environment variables
CLIENT_CARD = os.environ.get("CLIENT_CARD") # Client ID of the Azure AD app
CLIENT_SEC = os.environ.get("CLIENT_SEC") # Client secret of the Azure AD app
TENANT_ID = os.environ.get("TENANT_ID")
DATAVERSE_URL = os.environ.get("DATAVERSE_URL")
TABLE_NAME = os.environ.get("TABLE_NAME")
DAYS_BACK = int(os.environ.get("DAYS_BACK", 15))  # Default to 15 days if not set

# Validate required environment variables
required_vars = ["CLIENT_CARD", "CLIENT_SEC", "TENANT_ID", "DATAVERSE_URL", "TABLE_NAME"]
missing_vars = [var for var in required_vars if not os.environ.get(var)]
if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

# -------- DATE FILTER SETUP ----------
# Calculate date range for filtering records (last N days)
end_date = datetime.now(timezone.utc)
start_date = end_date - timedelta(days=DAYS_BACK)

# Format dates to ISO 8601 for Dataverse OData filter
start_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
end_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

# Build OData filter query
filter_query = f"?$filter=createdon ge {start_str} and createdon le {end_str}"

# -------- AUTHENTICATION ----------
# Set up Microsoft Authentication Library (MSAL) for client credentials flow
authority = f"https://login.microsoftonline.com/{TENANT_ID}"

app = ConfidentialClientApplication(
    CLIENT_CARD,
    authority=authority,
    client_credential=CLIENT_SEC,
)

# Acquire access token
token_response = app.acquire_token_for_client(scopes=[f"{DATAVERSE_URL}/.default"])
access_token = token_response.get("access_token")

if not access_token:
    raise Exception(f"Authentication failed: {token_response}")

# -------- API REQUEST ----------
# Construct the API URL for Dataverse table
url = f"{DATAVERSE_URL}/api/data/v9.2/{TABLE_NAME}{filter_query}"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
    "OData-MaxVersion": "4.0",
    "OData-Version": "4.0",
}

# Make the GET request
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    records = data.get("value", [])
    print(f"Found {len(records)} records from the last {DAYS_BACK} days.")

    # Process each record
    for i, row in enumerate(records, start=1):
        content_str = row.get("content")
        if not content_str:
            continue  # Skip if no content

        # Extract reactions from the conversation content
        reactions = reactionreader.extract_reaction_feedback(content_str)
        if reactions:
            #print(f"\nRecord {i}:")
            for reaction in reactions:
                print(json.dumps(reaction, indent=2))
else:
    print(f"API Error: {response.status_code} - {response.text}")

