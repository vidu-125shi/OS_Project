from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").timestamp()
    except ValueError as e:
        raise ValueError(f"Invalid time format: {time_str}. Expected format: YYYY-MM-DD HH:MM:SS")

@app.route('/simulate', methods=['POST'])
def simulate():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    try:
        file = request.files['file']
        algorithm = request.form.get('algorithm', 'fcfs')
        quantum_str = request.form.get('quantum', '0')
        quantum = int(quantum_str) if quantum_str.strip().isdigit() else 0

        data = json.load(file)
        
        if not isinstance(data, list):
            return jsonify({"error": "Invalid file format. Expected an array of processes"}), 400

        processes = []
        for idx, p in enumerate(data):
            try:
                processes.append({
                    'pid': p.get('process_id', idx + 1),
                    'arrival': parse_time(p['arrival_time']),
                    'burst': float(p['burst_time']),
                    'priority': int(p.get('priority', 0)),
                    'process_name': p.get('process_name', f'Process {idx + 1}')
                })
            except KeyError as e:
                return jsonify({"error": f"Missing required field in process {idx}: {str(e)}"}), 400
            except ValueError as e:
                return jsonify({"error": f"Invalid value in process {idx}: {str(e)}"}), 400
        
        # Normalize arrival times to start from 0
        if processes:
            min_arrival = min(p['arrival'] for p in processes)
            for p in processes:
                p['arrival'] = round(p['arrival'] - min_arrival, 2)

        result = run_algorithm(processes, algorithm, quantum)
        return jsonify(result)
        
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON file"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_algorithm(data, algorithm, quantum):
    processes = data.copy()

    if algorithm == 'fcfs':
        processes.sort(key=lambda x: x['arrival'])
    elif algorithm == 'sjf':
        processes.sort(key=lambda x: (x['arrival'], x['burst']))
    elif algorithm == 'priority':
        processes.sort(key=lambda x: (x['priority'], x['arrival']))
    elif algorithm == 'rr':
        return round_robin(processes, quantum)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    time = 0
    output = []
    total_wt = 0
    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        start = time
        time += p['burst']
        end = time
        wait = start - p['arrival']
        total_wt += wait
        output.append({
            "pid": p['pid'],
            "process_name": p['process_name'],
            "start": round(start, 2),
            "end": round(end, 2),
            "wait": round(wait, 2)
        })

    avg_wait = total_wt / len(processes) if processes else 0
    return {"gantt": output, "avg_waiting_time": round(avg_wait, 2)}

def round_robin(processes, quantum):
    from collections import deque
    queue = deque()
    processes = sorted(processes, key=lambda x: x['arrival'])
    time = 0
    output = []
    i = 0
    total_wt = 0
    
    while i < len(processes) or queue:
        while i < len(processes) and processes[i]['arrival'] <= time:
            processes[i]['remaining'] = processes[i]['burst']
            queue.append(processes[i])
            i += 1
            
        if queue:
            p = queue.popleft()
            exec_time = min(quantum, p['remaining'])
            start = time
            time += exec_time
            p['remaining'] -= exec_time
            
            if p['remaining'] <= 0:
                wait_time = start - p['arrival'] - (p['burst'] - p['remaining'])
                total_wt += wait_time
            
            output.append({
                "pid": p['pid'],
                "process_name": p['process_name'],
                "start": round(start, 2),
                "end": round(time, 2)
            })
            
            if p['remaining'] > 0:
                queue.append(p)
        else:
            time += 1
    
    avg_wait = total_wt / len(processes) if processes else 0
    return {"gantt": output, "avg_waiting_time": round(avg_wait, 2)}

if __name__ == '__main__':
    app.run(debug=True)