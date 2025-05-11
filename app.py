# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/simulate', methods=['POST'])
def simulate():
    file = request.files['file']
    algorithm = request.form['algorithm']
    quantum_str = request.form.get('quantum', '0')
    quantum = int(quantum_str) if quantum_str.strip().isdigit() else 0

    data = json.load(file)

    result = run_algorithm(data, algorithm, quantum)
    return jsonify(result)

def run_algorithm(data, algorithm, quantum):
    processes = data['processes']

    if algorithm == 'fcfs':
        processes.sort(key=lambda x: x['arrival'])
    elif algorithm == 'sjf':
        processes.sort(key=lambda x: x['burst'])
    elif algorithm == 'priority':
        processes.sort(key=lambda x: x['priority'])
    elif algorithm == 'rr':
        return round_robin(processes, quantum)

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
        output.append({"pid": p['pid'], "start": start, "end": end, "wait": wait})

    avg_wait = total_wt / len(processes)
    return {"gantt": output, "avg_waiting_time": avg_wait}

def round_robin(processes, quantum):
    from collections import deque
    queue = deque()
    processes = sorted(processes, key=lambda x: x['arrival'])
    time = 0
    output = []
    i = 0
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
            output.append({"pid": p['pid'], "start": start, "end": time})
            if p['remaining'] > 0:
                queue.append(p)
        else:
            time += 1
    return {"gantt": output}

if __name__ == '__main__':
    app.run(debug=True)
