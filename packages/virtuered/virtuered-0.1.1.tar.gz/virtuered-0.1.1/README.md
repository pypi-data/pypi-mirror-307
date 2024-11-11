# VirtueRed CLI

Command line interface for VirtueAI Redteaming system.

## Installation

```bash
pip install virtuered
```

## Usage

First, ensure the VirtueRed server is running in Docker:

```bash
sudo docker run -d --cap-add=SYS_PTRACE -p 4401:4401 \
    -v /path/to/log:/app/log \
    -v /path/to/runs:/app/runs \
    --gpus all virtuered_nv
```

Then you can use the CLI:

```bash
# List all runs
virtuered list

# Monitor ongoing scans
virtuered monitor

# Get summary of a run
virtuered summary test_scan

# Pause/Resume a scan
virtuered pause 1
virtuered resume test_scan

# Generate report
virtuered report test_scan

# Delete a run
virtuered delete 1
```

For custom server URL:
```bash
virtuered --server http://localhost:4401 list
```

## Commands

- `list`: Show all runs
- `monitor`: Monitor ongoing scans
- `summary`: Get detailed summary of a run
- `report`: Generate PDF report
- `pause`: Pause a running scan
- `resume`: Resume a paused scan
- `delete`: Delete a run

## Development

To install in development mode:
```bash
git clone https://github.com/yourusername/virtuered.git
cd virtuered
pip install -e .
```