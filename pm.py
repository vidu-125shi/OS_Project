import psutil
import json
import time
from datetime import datetime

def monitor_process(process_name, output_file='process_stats.json', interval=1):
    """
    Monitor a process and record its CPU allocation stats.
    
    Args:
        process_name (str): Name of the process to monitor
        output_file (str): Path to save the JSON output
        interval (int): Monitoring interval in seconds
    """
    process_data = []
    
    try:
        while True:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_times', 'create_time', 'nice']):
                if proc.info['name'] == process_name:
                    # Get process information
                    pid = proc.info['pid']
                    create_time = proc.info['create_time']
                    cpu_times = proc.info['cpu_times']
                    priority = proc.info['nice']  # Unix priority (nice value)
                    
                    # Calculate arrival time (relative to script start)
                    arrival_time = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Calculate burst time (CPU time used so far)
                    burst_time = cpu_times.user + cpu_times.system
                    
                    # Record the data
                    record = {
                        'process_id': pid,
                        'process_name': process_name,
                        'arrival_time': arrival_time,
                        'burst_time': burst_time,
                        'priority': priority,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    process_data.append(record)
                    print(f"Recorded: {record}")
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user. Saving data...")
        with open(output_file, 'w') as f:
            json.dump(process_data, f, indent=2)
        print(f"Data saved to {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor process CPU allocation')
    parser.add_argument('process_name', help='Name of the process to monitor')
    parser.add_argument('--output', default='process_stats.json', 
                       help='Output JSON file path')
    parser.add_argument('--interval', type=float, default=1.0,
                       help='Monitoring interval in seconds')
    
    args = parser.parse_args()
    
    print(f"Starting to monitor process: {args.process_name}")
    print(f"Data will be saved to: {args.output}")
    print(f"Monitoring interval: {args.interval} seconds")
    print("Press Ctrl+C to stop monitoring and save data...")
    
    monitor_process(args.process_name, args.output, args.interval)