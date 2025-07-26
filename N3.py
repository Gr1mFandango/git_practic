import re
from collections import defaultdict
import math

filename = 'input.txt'

times = defaultdict(list)
total_requests = 0
error_5xx_requests = 0

def percentile_75(data):
    data_sorted = sorted(data)
    k = int(math.ceil(0.75 * len(data_sorted))) - 1  
    return data_sorted[k]

with open(filename, encoding='utf-8') as f:
    for line in f:
        if '/pet' not in line:
            continue

        match = re.search(r'HTTP/\S+\s+(\d{3})', line)
        if not match:
            continue
        code = match.group(1)

        time_match = re.search(r'(\d+)ms$', line.strip())
        if not time_match:
            continue
        time_ms = int(time_match.group(1))

        times[code].append(time_ms)
        total_requests += 1
        if code.startswith('5'):
            error_5xx_requests += 1

for code in sorted(times.keys()):
    count = len(times[code])
    min_t = min(times[code])
    max_t = max(times[code])
    p75 = percentile_75(times[code])
    print(f"{code} {count} {min_t} {max_t} {p75}")

error_percent = int((error_5xx_requests / total_requests) * 100) if total_requests else 0
print(error_percent)

