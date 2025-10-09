# LabOps

A Python CLI tool for managing datacenter lab resources (hosts, racks, switches).
Built to streamline troubleshooting and inventory navigation with formatted output
and powerful filtering capabilities for datacenter operations.

## Features

- **Host Management**: List, filter, and lookup hosts by multiple criteria
- **Rack Operations**: View rack contents and host positioning
- **Interactive TUI**: Full-screen terminal interface for visual exploration
- **Advanced Filtering**: Status, platform, BMC, lab, and fuzzy matching
- **Performance Optimized**: 5-minute caching system for instant responses
- **Professional Output**: Clean, formatted display with color coding
- **API Integration**: Direct connection to hardware tracking systems

## Setup

```bash
git clone https://github.com/your-username/labops.git
cd labops
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with your API credentials:
```bash
API_BASE_URL=https://your-api-endpoint.com/api/v1/track
API_KEY=your-api-key-here
```

## Usage Examples

### Host Operations
```bash
# List all available hosts
labops hosts --available

# Find hosts by platform (with fuzzy matching)
labops hosts --platform dell

# Filter by multiple criteria
labops hosts --status Available --bmc --limit 10

# Lookup specific host
labops 1234567890
```

### Rack Operations
```bash
# List all racks in a lab
labops racks --location LAB01

# View specific rack contents
labops rack R1-A01

# List racks with limit
labops racks --limit 5
```

### Interactive Terminal UI
```bash
# Launch interactive TUI for visual exploration
labops tui
```

### System Overview
```bash
# Datacenter summary
labops summary
```

## Example Output

### Host Lookup
```bash
$ labops 1234567890
```
```
Asset ID: 1234567890
Status: Available
Location: DC1.R1-A01.15

Platform: DELL-R740
Manufacturer: DELL
Hardware ID: DL.R740-ABC123

Console IP: 10.1.100.50

Rack Info:
  Lab: LAB01
  Position: DC1.R1-A01
  VLAN ID: 100
  Subnet: 10.1.0.0/24

Usage Type: General Use
```

### Rack Contents
```bash
$ labops rack R1-A01
```
```
Rack Position: R1-A01
Lab: LAB01
Host Count: 5

Hosts by Status:
  Available: 4
  Reserved: 1

Hosts in Rack:

Asset ID     Hardware ID          Platform        BMC IP          LAN IP
-----------------------------------------------------------------------------
1234567890   DL.R740-ABC123       DELL-R740       10.1.100.50     10.1.200.50
1234567891   HP.DL380-XYZ456      HP-DL380        10.1.100.51     10.1.200.51
1234567892   SM.X11-DEF789        SUPERMICRO-X11  10.1.100.52     N/A
1234567893   DL.R640-GHI012       DELL-R640       10.1.100.53     10.1.200.53
1234567894   HP.DL360-JKL345      HP-DL360        N/A             10.1.200.54
```

### Host Filtering
```bash
$ labops hosts --platform DELL --limit 5
```
```
Showing: 5 of 127 total hosts

Asset ID: 1234567890
Status: Available
Location: DC1.R1-A01.15

Platform: DELL-R740
Manufacturer: DELL
Console IP: 10.1.100.50
LAN IP: 10.1.200.50

--------------------------------------------------

Total Hosts: 5
```

### Interactive TUI
```bash
$ labops tui
```
```
┌─ SEALAB85 Racks ─────────────────────┐┌─ Rack SEA85.159.R6-L01 ──────────────┐
│ ▶ SEA85.159 (12 racks, 180 hosts)   ││ Rack: SEA85.159.R6-L01               │
│ ▼ SEA85.6920 (8 racks, 95 hosts)    ││ Lab: SEALAB85                        │
│   ▶ SEA85.6920.R1-A01 (15 hosts)    ││ Host Count: 15                       │
│   ▼ SEA85.6920.R1-A02 (12 hosts)    ││                                      │
│     └─ 1703827523: HUMBOLDT21       ││ Hosts in Rack (15):                 │
│     └─ 1703827484: HUMBOLDT21       ││   • 1703827523: HUMBOLDT21 [Avail]  │
│     └─ ... and 10 more hosts        ││     Console IP: 172.16.76.116       │
│                                      ││   • 1703827484: HUMBOLDT21 [Avail]  │
└──────────────────────────────────────┘└──────────────────────────────────────┘

Navigation: Arrow keys, Enter to expand/select, 'q' to quit
```

## Interface Options

**Command Line Interface (CLI)** - Perfect for automation and scripting:
- Fast, direct commands
- Scriptable and pipeable output
- Great for experienced users

**Terminal User Interface (TUI)** - Perfect for exploration and discovery:
- Visual hierarchy of rooms → racks → hosts
- Interactive browsing with keyboard navigation
- Expandable tree view with detailed panels
- Great for discovering available resources
