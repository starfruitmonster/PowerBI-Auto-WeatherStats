# PowerBI-Auto-WeatherStats
Creates an automated script that pings the powerbi api every 2 hours

# WeatherStats: Power BI E5 Auto-Renew Program

**WeatherStats** is an automation program that helps keep your **Microsoft 365 E5 Developer Tenant** active by simulating realistic usage of Power BI. It achieves this by:

- Creating a push dataset via the Power BI REST API
- Inserting new rows of data (timestamp, simulated weather, location)
- Triggering a dataset refresh
- Running every 3 hours via GitHub Actions, or manually on demand

## Prerequisites

- Microsoft 365 E5 Developer account
- Power BI Desktop (only needed for visualization)
- Azure AD App Registration
- GitHub account with a Personal Access Token (PAT)
- Python 3.9+ and the `requests` library

## Step 1: Register Azure AD Application

1. Go to https://portal.azure.com
2. Navigate to Azure Active Directory > App registrations > New registration
   - Name: WeatherStats-App
   - Redirect URI: http://localhost:53682/
   - Supported account types: Multitenant
3. After registration, note your Client ID and Tenant ID

### Create a client secret

- Go to Certificates & secrets > New client secret
- Copy the generated secret value

### Set API permissions

Power BI Service:
  - Dataset.ReadWrite.All
  - Workspace.Read.All

Microsoft Graph:
  - offline_access
  - openid

After setting, click "Grant admin consent"

## Step 2: Create WeatherStats Workspace

Open Power BI Web, go to Workspaces > New Workspace > Workspace Name: WeatherStats Workspace

## Step 3: Generate a Refresh Token

Download and use the included `obtain refresh token.py` script, changing CLIENT ID and CLIENT SECRET to that found above to obtain the refresh and access tokens. It would be printed in a txt file.

## Step 4: Create a Push Dataset

Download and use the included `create_dataset.py` script, changing CLIENT ID, CLIENT SECRET and REFRESH TOKEN to create a Power BI push dataset. It defines a table called WeatherStats with the following fields:

- Date (string)
- Time (string)
- Temperature (Int64)
- Location (string)

## Step 5: GitHub Personal Access Token Setup

Click your profile icon, go to Settings > Developer Settings > Personal Access Tokens > Tokens (Classic) > Generate a new token (Classic) > Select repo_hook, repo, workflow.

Save the PAT Token Code

## Step 6: GitHub Repository Setup

Go to REPO Settings > Secrets and variables > Actions, then add the following secrets:

- CONFIG_ID: Azure Client ID
- CONFIG_KEY: Azure Client Secret
- REFRESH_TOKEN: Your refresh token
- GH_TOKEN: GitHub Personal Access Token (PAT)

## Step 7: Python Script (weatherstats.py)

This script:
- Authenticates to Azure
- Finds your Power BI workspace and dataset
- Pushes a row of weather/timestamp data
- Triggers a refresh

## Step 8: Testing and Validation

- Go to GitHub > Actions tab
- Click Run Workflow
- Confirm the Action runs successfully
- Check Power BI Service > WeatherStats Workspace:
  - Dataset has new rows
  - Dataset refreshes appear in refresh history
