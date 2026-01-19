import os
import sys
import time
import argparse
import datetime

def get_directory_stats(path):
    """
    Recursively calculates the total size and file count of a directory.
    Returns: (total_size_bytes, total_file_count)
    """
    total_size = 0
    total_count = 0
    try:
        if os.path.isfile(path):
             return os.path.getsize(path), 1

        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    # Skip symbolic links
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
                        total_count += 1
                except OSError:
                    # Permission error or file disappeared
                    pass
    except OSError as e:
        print(f"Error accessing path: {e}")
        return 0, 0

    return total_size, total_count

def format_size(size_bytes):
    """Formats bytes into human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def format_duration(seconds):
    """Formats seconds into human readable string."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{int(h)}h {int(m)}m {int(s)}s"
    elif m > 0:
        return f"{int(m)}m {int(s)}s"
    else:
        return f"{s:.2f}s"

def main():
    parser = argparse.ArgumentParser(description="Monitor file growth (size and count) over a duration.")
    parser.add_argument("--path", type=str, required=True, help="Target path to monitor (recursive).")
    parser.add_argument("--duration", type=float, required=True, help="Duration to run the script in hours.")

    args = parser.parse_args()

    target_path = args.path
    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' does not exist.")
        sys.exit(1)

    duration_hours = args.duration
    duration_seconds = duration_hours * 3600

    print(f"Starting File Growth Monitor")
    print(f"Target Path: {target_path}")
    print(f"Duration: {duration_hours} hours ({duration_seconds} seconds)")
    print("Calculating initial stats... please wait.")

    start_time = time.time()
    start_size, start_count = get_directory_stats(target_path)

    print(f"Initial Size: {format_size(start_size)}")
    print(f"Initial File Count: {start_count}")
    print(f"Monitoring started at {datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print("Press Ctrl+C to stop early (report will be generated).")

    try:
        # Loop until duration expires
        while time.time() - start_time < duration_seconds:
            time.sleep(1) # Check every second
            # Optional: update progress bar or spinner?
            # Keeping it simple as requested "output report ... beautiful" -> final report.
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("\nCalculating final stats... please wait.")
    end_size, end_count = get_directory_stats(target_path)

    # Calculations
    size_growth = end_size - start_size
    count_growth = end_count - start_count

    # Rates
    if elapsed_time > 0:
        growth_rate_per_sec = size_growth / elapsed_time
        count_rate_per_sec = count_growth / elapsed_time
    else:
        growth_rate_per_sec = 0
        count_rate_per_sec = 0

    # Forecasts
    seconds_in_day = 86400
    seconds_in_month = 86400 * 30
    seconds_in_year = 86400 * 365

    forecast_day = growth_rate_per_sec * seconds_in_day
    forecast_month = growth_rate_per_sec * seconds_in_month
    forecast_year = growth_rate_per_sec * seconds_in_year

    forecast_count_day = count_rate_per_sec * seconds_in_day

    # Generate Report
    lines = []
    lines.append("==================================================")
    lines.append("              FILE GROWTH REPORT                  ")
    lines.append("==================================================")
    lines.append(f"Target Path      : {target_path}")
    lines.append(f"Start Time       : {datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"End Time         : {datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Actual Duration  : {format_duration(elapsed_time)}")
    lines.append("-" * 50)
    lines.append("GROWTH STATISTICS")
    lines.append("-" * 50)
    lines.append(f"{'Metric':<20} | {'Start':<15} | {'End':<15} | {'Growth (Net)':<15}")
    lines.append("-" * 76)
    lines.append(f"{'Size':<20} | {format_size(start_size):<15} | {format_size(end_size):<15} | {format_size(size_growth):<15}")
    lines.append(f"{'File Count':<20} | {str(start_count):<15} | {str(end_count):<15} | {str(count_growth):<15}")
    lines.append("-" * 76)
    lines.append(f"Growth Rate      : {format_size(growth_rate_per_sec)}/sec ({format_size(growth_rate_per_sec*3600)}/hour)")
    lines.append("-" * 50)
    lines.append("FORECAST (Based on actual run rate)")
    lines.append("-" * 50)
    lines.append(f"1 Day Growth     : {format_size(forecast_day)}")
    lines.append(f"30 Days Growth   : {format_size(forecast_month)}")
    lines.append(f"1 Year Growth    : {format_size(forecast_year)}")
    lines.append("==================================================")

    report_content = "\n".join(lines)
    print(report_content)

    # Save to file
    filename = f"growth_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"\nReport saved to: {filename}")
    except OSError as e:
        print(f"\nError saving report: {e}")

if __name__ == "__main__":
    main()
