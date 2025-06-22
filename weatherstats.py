import requests, os, datetime

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
refresh_token = os.getenv("REFRESH_TOKEN")
tenant_id = os.getenv("TENANT_ID", "common")

# Step 1: Get Access Token
token_res = requests.post(
    f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    }
)
access_token = token_res.json().get("access_token")
if not access_token:
    print("Token error:", token_res.text)
    exit(1)

headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
pbi_url = "https://api.powerbi.com/v1.0/myorg"

# Step 2: Get workspace
groups = requests.get(f"{pbi_url}/groups", headers=headers).json()["value"]
workspace = next((g for g in groups if g["name"] == "WeatherStats Workspace"), None)
if not workspace:
    print("Workspace not found.")
    exit(1)
group_id = workspace["id"]

# Step 3: Get dataset
datasets = requests.get(f"{pbi_url}/groups/{group_id}/datasets", headers=headers).json()["value"]
dataset = next((d for d in datasets if d["name"] == "WeatherStats"), None)
if not dataset:
    print("Dataset not found.")
    exit(1)
dataset_id = dataset["id"]

# Step 4: Push new row
now = datetime.datetime.now()
row_data = {
    "rows": [{
        "Date": now.strftime("%Y-%m-%d"),
        "Time": now.strftime("%H:%M:%S"),
        "Temperature": 30 + (now.minute % 5),
        "Location": "Singapore"
    }]
}
push_url = f"{pbi_url}/groups/{group_id}/datasets/{dataset_id}/tables/WeatherStats/rows"
res = requests.post(push_url, headers=headers, json=row_data)
print("Push row result:", res.status_code, res.text)

# Step 5: Refresh (optional but included for realism)
refresh_url = f"{pbi_url}/groups/{group_id}/datasets/{dataset_id}/refreshes"
r = requests.post(refresh_url, headers=headers)
print("Refresh status:", r.status_code)
