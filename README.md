# File Monitor Script

This is a Python script designed to monitor a specific directory for file activity. It calculates the average number of files over specified time intervals and tracks the net change in the number of files.

## Features

- **Monitor Total Files**: Tracks the number of files in a directory over time.
- **Calculate Averages**: Reports the average total files at user-defined time intervals (e.g., first 5 minutes, 10 minutes).
- **Calculate File Count Difference**: Reports the difference in the number of files between the start and end of the monitoring period.
- **Recursive Option**: Supports monitoring subdirectories.
- **Environment Variable Configuration**: Path is set via an environment variable.

## Prerequisites

- Python 3.x

## Usage

### 1. Set the Environment Variable

Set the `MONITOR_PATH` environment variable to the directory you want to monitor.

**Linux/macOS:**
```bash
export MONITOR_PATH=/path/to/your/directory
```

**Windows (Command Prompt):**
```cmd
set MONITOR_PATH=C:\path\to\your\directory
```

### 2. Run the Script

Run the script using Python, providing the required arguments:

```bash
python file_monitor.py --duration <minutes> --intervals <m1> <m2> ... [--recursive]
```

#### Arguments:

- `--duration`: (Required) The total duration to run the monitor, in minutes.
- `--intervals`: (Required) A list of time points (in minutes) at which to calculate the average total files.
- `--recursive`: (Optional) If set, the script will also count files in subdirectories.

### Examples

**Example 1: Basic Monitoring**
Run for 10 minutes, calculate average at 5 minutes and 10 minutes.

```bash
export MONITOR_PATH=./data
python file_monitor.py --duration 10 --intervals 5 10
```

**Example 2: Recursive Monitoring**
Run for 60 minutes, check subdirectories, and get averages at 15, 30, and 60 minutes.

```bash
export MONITOR_PATH=./logs
python file_monitor.py --duration 60 --intervals 15 30 60 --recursive
```

## Output Format

The script will output a summary report after the duration ends or upon interruption (Ctrl+C).

```text
========================================
             FINAL REPORT
========================================
Monitoring Path: ./data
Total Execution Time: 10.00 minutes
----------------------------------------
Average Total Files:
  - @ 5.0 min: 120.50
  - @ 10.0 min: 115.20
----------------------------------------
File Count Difference:
  - Start: 100
  - End: 110
  - Difference: 10 (End - Start)
========================================
```
