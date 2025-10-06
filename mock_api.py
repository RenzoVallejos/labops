from fastapi import FastAPI, Header, HTTPException
import uvicorn

app = FastAPI()

# Fake API key for local testing
API_KEY = "mock-secret-token"

# Fake data
hosts = [
    {"asset_id": "8401000103", "hostname": "web-01", "status": "available", "platform": "x86", "rack": "R01", "switch": "S01"},
    {"asset_id": "8401000104", "hostname": "db-01", "status": "in-use", "platform": "arm64", "rack": "R02", "switch": "S02"}
]

racks = [
    {"rack_id": "R01", "location": "west-dc", "capacity": "42U", "used": "30U"},
    {"rack_id": "R02", "location": "east-dc", "capacity": "42U", "used": "40U"}
]

switches = [
    {"switch_id": "S01", "rack": "R01", "ports": 48, "used_ports": 32, "status": "active", "model": "Cisco-9300"},
    {"switch_id": "S02", "rack": "R02", "ports": 48, "used_ports": 45, "status": "active", "model": "Juniper-EX"}
]

# Middleware: require API token
def check_auth(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.get("/hosts")
def get_hosts(x_api_key: str = Header(...)):
    check_auth(x_api_key)
    return hosts

@app.get("/racks")
def get_racks(x_api_key: str = Header(...)):
    check_auth(x_api_key)
    return racks

@app.get("/switches")
def get_switches(x_api_key: str = Header(...)):
    check_auth(x_api_key)
    return switches

# Entry point for running directly
if __name__ == "__main__":
    uvicorn.run("mock_api:app", host="127.0.0.1", port=5000, reload=True)

