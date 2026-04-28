# Dataverse Conversation Reader

A Python script to extract conversation transcripts and user reactions from Microsoft Dataverse.

## Overview

This project connects to Microsoft Dataverse, retrieves conversation transcripts from the last N days, and extracts user reactions (like/dislike) along with feedback text.

## Features

- **Dataverse Integration**: Connects to Microsoft Dataverse using MSAL authentication
- **Date Range Filtering**: Retrieves records from the last N days (configurable)
- **Reaction Extraction**: Extracts user reactions (like/dislike) from conversation activities
- **Feedback Capture**: Collects user feedback text associated with reactions
- **User Tracking**: Records the Azure AD Object ID and timestamp of reactions

## Prerequisites

- Python 3.8+
- Microsoft Dataverse instance
- Service principal credentials (Client ID and Client Secret)
- Tenant ID

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd dataversereader
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root with the following variables:
   ```
   CLIENT_CARD=<your-client-id>
   CLIENT_SAMPLE=<your-client-secret>
   TENANT_ID=<your-tenant-id>
   DATAVERSE_URL=https://<org>.crm.dynamics.com
   TABLE_NAME=conversationtranscripts
   DAYS_BACK=15
   ```

## Usage

Run the script to fetch and process conversation records:

```bash
python dataverseConvReader.py
```

The script will:
1. Authenticate with Dataverse
2. Query records from the last N days
3. Extract reactions and feedback
4. Output the results in JSON format

## Project Structure

```
dataversereader/
├── dataverseConvReader.py      # Main script
├── dataversesample1.py          # Sample implementation
├── reactionreader.py            # Reaction extraction module
├── dvreaderv1.cs               # C# reference implementation
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration (not in git)
└── .gitignore                   # Git ignore rules
```

## Functions

### `extract_reaction_feedback(content_json, reactions_to_extract=None)`

Extracts feedback for specified reactions from conversation activities.

**Parameters:**
- `content_json` (str, bytes, bytearray, or dict): The JSON content of the conversation
- `reactions_to_extract` (list, optional): List of reaction types to extract (default: `['dislike', 'like']`)

**Returns:**
- List of dictionaries containing reaction details with keys:
  - `reaction`: Type of reaction
  - `feedbackText`: User's feedback text
  - `user_aadObjectId`: Azure AD Object ID of the user
  - `timestamp`: Timestamp of the activity

## Error Handling

The script validates required environment variables and will exit with an error message if any are missing.

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
