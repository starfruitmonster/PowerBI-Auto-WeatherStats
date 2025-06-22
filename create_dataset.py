import requests
import os

# Set environment variables or replace directly
client_id = os.getenv("CLIENT_ID", "YOUR CLIENT ID")
client_secret = os.getenv("CLIENT_SECRET", "YOUR CLIENT SECRET")
refresh_token = os.getenv("REFRESH_TOKEN", "REFRESH TOKEN")
tenant_id = os.getenv("TENANT_ID", "common")

# Define target workspace name
workspace_name = "WeatherStats Workspace"

# Step 1: Get Access Token
print("Requesting access token...")
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_res = requests.post(token_url, data={
    "client_id": client_id,
    "client_secret": client_secret,
    "refresh_token": refresh_token,
    "grant_type": "refresh_token",
    "scope": "https://analysis.windows.net/powerbi/api/.default"
})
access_token = token_res.json().get("access_token")
if not access_token:
    print("Failed to get token:", token_res.text)
    exit(1)

headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
pbi_url = "https://api.powerbi.com/v1.0/myorg"

# Step 2: Get Workspace ID
print(f"Looking for workspace: {workspace_name}")
groups = requests.get(f"{pbi_url}/groups", headers=headers).json()["value"]
workspace = next((g for g in groups if g["name"] == workspace_name), None)

if not workspace:
    print(f"Workspace '{workspace_name}' not found. Please create it manually on Power BI Service.")
    exit(1)

group_id = workspace["id"]
print("Workspace found:", group_id)

# Step 3: Create Dataset
print("Creating dataset 'WeatherStats'...")

dataset_definition = {
    "name": "WeatherStats",
    "tables": [
        {
            "name": "WeatherStats",
            "columns": [
                {"name": "Date", "dataType": "string"},
                {"name": "Time", "dataType": "string"},
                {"name": "Temperature", "dataType": "Int64"},
                {"name": "Location", "dataType": "string"}
            ]
        }
    ],
    "defaultMode": "Push"  # this ensures push dataset type
}

create_url = f"{pbi_url}/groups/{group_id}/datasets?defaultRetentionPolicy=basicFIFO"
res = requests.post(create_url, headers=headers, json=dataset_definition)

if res.status_code == 201:
    print("Dataset 'WeatherStats' created successfully.")
else:
    print("Failed to create dataset:", res.status_code)
    print(res.text)
