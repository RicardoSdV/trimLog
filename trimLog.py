import re
from pathlib import Path
from time import time

start_time = time()

log_dir_path = Path(r'C:\.prjs\trimLog\logs_dir_example')
log_paths = log_dir_path.glob('**/*.log')

force_retrim = False

for log_path in log_paths:
    if log_path.name.startswith('t_'): continue

    trimmed_log_path = log_path.with_name('t_' + log_path.name)
    if trimmed_log_path.exists() and not force_retrim: continue

    with open(log_path, 'r') as f:
        lines = f.readlines()

    if len(lines) < 1: continue

    log_pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3,4}): (DEBUG:|INFO:|WARNING:|ERROR:).*$"

    for i, line in enumerate(lines):
        match = re.match(log_pattern, line)
        if match:
            ymd, hour, minute, sec, msec, log_flag = match.groups()

            line = line.replace(
                '{}{}{}{}{}{}{}{}{}{}{}{}'.format(
                    ymd, ' ', hour, ':', minute, ':', sec, '.', msec, ': ', log_flag, ' '
                ), '')

            lines[i] = line

    compressed_lines = []
    consecutive_count = 1
    previous_line = lines[0]

    for line in lines[1:]:
        if line == previous_line:
            consecutive_count += 1
        else:
            if consecutive_count > 1:
                compressed_lines.append(f'{consecutive_count}x {previous_line}')
            else:
                compressed_lines.append(previous_line)
            consecutive_count = 1
            previous_line = line

    if consecutive_count > 1:
        compressed_lines.append(f"{consecutive_count}x {previous_line}")
    else:
        compressed_lines.append(previous_line)


    with open(trimmed_log_path, 'w') as f:
        f.writelines(compressed_lines)


print('Done trimming, took:', time() - start_time)
