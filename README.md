# LabOps

A Python CLI tool for managing datacenter lab resources (hosts, racks, switches).
Built to make troubleshooting and inventory navigation easier — returns data in clean JSON,
ready for scripting with `jq` or automation pipelines.
## Features
- List hosts, racks, and switches
- Lookup a host by asset ID
- Show rack contents (hosts + switches in one view)
- Summarize datacenter health (host status, rack usage, switch utilization)
- JSON-first output for automation
- Configurable via `.env` (API URL, API Key)

## Setup
```bash
git clone https://github.com/your-username/labops.git
cd /filepath/labops
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
pip 
install -r requirements.txt 
```
## Example Usage
```bash
# List all hosts
labops hosts

# Lookup a single host
labops host --asset-id 8401000103

# Show contents of a rack
labops rack-contents --rack-id R01

# Summary view
labops summary | jq .

```
## Example Output
```bash
{
  "hosts": {
    "total": 2,
    "by_status": {
      "available": 1,
      "in-use": 1
    }
  },
  "racks": {
    "total": 2
  },
  "switches": {
    "total": 2,
    "by_model": {
      "Cisco-9300": 1,
      "Juniper-EX": 1
    }
  }
}
```
