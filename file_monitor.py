import os
import sys
import time
import argparse
import statistics
from datetime import datetime

def get_files(path, recursive):
    """
    Returns a set of file paths in the given directory.
    """
    file_set = set()
    try:
        if recursive:
            for root, dirs, files in os.walk(path):
                for f in files:
                    file_set.add(os.path.join(root, f))
        else:
            if os.path.exists(path):
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    if os.path.isfile(full_path):
                        file_set.add(full_path)
            else:
                print(f"Error: Path '{path}' does not exist.")
                sys.exit(1)
    except OSError as e:
        print(f"Error accessing path: {e}")
        sys.exit(1)
    return file_set

def format_duration(seconds):
    return f"{seconds:.2f} seconds"

def main():
    parser = argparse.ArgumentParser(description="Monitor file statistics in a directory.")
    parser.add_argument("--duration", type=float, required=True, help="Duration to run the monitor in minutes.")
    parser.add_argument("--intervals", type=float, nargs='+', required=True, help="Time intervals (in minutes) to calculate average total files.")
    parser.add_argument("--recursive", action="store_true", help="Include subdirectories in the scan.")

    args = parser.parse_args()

    monitor_path = os.environ.get("MONITOR_PATH")
    if not monitor_path:
        print("Error: Environment variable 'MONITOR_PATH' is not set.")
        print("Please set it before running the script. Example: export MONITOR_PATH=/path/to/monitor")
        sys.exit(1)

    if not os.path.isdir(monitor_path):
        print(f"Error: The path '{monitor_path}' is not a valid directory.")
        sys.exit(1)

    print(f"Starting monitor on: {monitor_path}")
    print(f"Recursive: {args.recursive}")
    print(f"Duration: {args.duration} minutes")
    print(f"Intervals for Avg Total: {args.intervals} minutes")
    print("Monitoring... (Press Ctrl+C to stop early, report will be generated based on elapsed time)")

    start_time = time.time()
    end_time = start_time + (args.duration * 60)

    # Sort intervals to ensure we check them in order if needed,
    # though for post-calculation it doesn't matter much.
    target_intervals = sorted(args.intervals)

    # Data storage
    # history: list of (timestamp, count)
    history = []

    # Initial scan
    current_files = get_files(monitor_path, args.recursive)
    initial_count = len(current_files)
    history.append((time.time(), initial_count))

    try:
        while time.time() < end_time:
            # Sleep for a short duration (e.g., 1 second)
            time.sleep(1)

            now = time.time()
            new_files_set = get_files(monitor_path, args.recursive)

            current_files = new_files_set
            history.append((now, len(current_files)))

            # Optional: Print simple progress or keep silent
            # print(f"\rTime remaining: {int(end_time - now)}s | Files: {len(current_files)}", end="")

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

    final_time = time.time()
    elapsed_seconds = final_time - start_time
    elapsed_minutes = elapsed_seconds / 60.0

    print("\n\n" + "="*40)
    print("             FINAL REPORT             ")
    print("="*40)
    print(f"Monitoring Path: {monitor_path}")
    print(f"Total Execution Time: {elapsed_minutes:.2f} minutes")
    print("-" * 40)

    # 1. Avg Total Files per Interval
    print("Average Total Files:")

    # Ensure we cover the recorded history relative to start_time
    # history stores (absolute_timestamp, count)

    for minutes in target_intervals:
        cutoff_seconds = minutes * 60
        # Filter history points that happened within this interval
        relevant_counts = [count for ts, count in history if ts - start_time <= cutoff_seconds]

        if relevant_counts:
            avg_count = statistics.mean(relevant_counts)
            print(f"  - @ {minutes} min: {avg_count:.2f}")
        else:
            print(f"  - @ {minutes} min: N/A (Not enough data)")

    print("-" * 40)

    # 2. File Count Difference
    final_count = len(current_files)
    count_diff = final_count - initial_count

    print("File Count Difference:")
    print(f"  - Start: {initial_count}")
    print(f"  - End: {final_count}")
    print(f"  - Difference: {count_diff} (End - Start)")

    print("="*40)

if __name__ == "__main__":
    main()
