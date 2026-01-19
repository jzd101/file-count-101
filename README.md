# File Monitoring Scripts

This repository contains Python scripts for monitoring file activity and growth in directories.

1. `file_monitor.py`: Monitors file count activity (average counts, net change) over short intervals.
2. `file_growth.py`: Measures data size growth (and file count) over a duration and forecasts future growth.

## Prerequisites

- Python 3.x

---

# Script 1: File Monitor (`file_monitor.py`)

Designed to monitor a specific directory for file activity. It calculates the average number of files over specified time intervals and tracks the net change in the number of files.

## Features

- **Monitor Total Files**: Tracks the number of files in a directory over time.
- **Calculate Averages**: Reports the average total files at user-defined time intervals.
- **Calculate File Count Difference**: Reports the difference in the number of files between start and end.
- **Recursive Option**: Supports monitoring subdirectories.
- **Flexible Configuration**: Path can be set via command-line argument or environment variable.

## Usage

### 1. Run the Script

```bash
python file_monitor.py --path <path> --duration <minutes> --intervals <m1> <m2> ... [--recursive]
```

#### Arguments:

- `--path`: (Optional) Path to the directory to monitor. Overrides `MONITOR_PATH` environment variable.
- `--duration`: (Required) The total duration to run the monitor, in minutes.
- `--intervals`: (Required) A list of time points (in minutes) at which to calculate the average total files.
- `--recursive`: (Optional) If set, the script will also count files in subdirectories.

*Note: If `--path` is not provided, the script looks for the `MONITOR_PATH` environment variable.*

### Examples

**Example 1: Basic Monitoring using Argument**
Run for 10 minutes, calculate average at 5 and 10 minutes.

```bash
python file_monitor.py --path ./data --duration 10 --intervals 5 10
```

**Example 2: Using Environment Variable**

```bash
export MONITOR_PATH=./logs
python file_monitor.py --duration 60 --intervals 15 30 60 --recursive
```

## Output Format

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

---

# Script 2: File Growth Monitor (`file_growth.py`)

Designed to measure how much data size (and file count) grows in a directory over a specific period. It provides a detailed report with growth rates and future forecasts.

## Features

- **Measure Net Growth**: Calculates the total size increase/decrease (files and folders recursively).
- **Growth Forecast**: Projects growth for 1 Day, 30 Days, and 1 Year based on the observed rate.
- **Detailed Report**: Outputs a readable report to the console and saves it to a text file.
- **Recursive**: Automatically scans all subdirectories.

## Usage

```bash
python file_growth.py --path <path> --duration <hours>
```

#### Arguments:

- `--path`: (Required) Target path to monitor.
- `--duration`: (Required) Duration to run the script, in hours (e.g., `1` for 1 hour, `0.5` for 30 minutes).

### Example

Monitor the `./incoming_data` folder for 1 hour:

```bash
python file_growth.py --path ./incoming_data --duration 1
```

## Output Format

The script prints a report to the console and saves a file named `growth_report_<timestamp>.txt`.

```text
==================================================
              FILE GROWTH REPORT
==================================================
Target Path      : ./incoming_data
Start Time       : 2024-04-27 10:00:00
End Time         : 2024-04-27 11:00:00
Actual Duration  : 1h 0m 0s
--------------------------------------------------
GROWTH STATISTICS
--------------------------------------------------
Metric               | Start           | End             | Growth (Net)
----------------------------------------------------------------------------
Size                 | 100.00 MB       | 150.00 MB       | 50.00 MB
File Count           | 1000            | 1500            | 500
----------------------------------------------------------------------------
Growth Rate      : 14.22 KB/sec (50.00 MB/hour)
--------------------------------------------------
FORECAST (Based on actual run rate)
--------------------------------------------------
1 Day Growth     : 1.17 GB
30 Days Growth   : 35.16 GB
1 Year Growth    : 427.73 GB
==================================================
```
