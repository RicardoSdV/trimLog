"""
How to use: Paste the path in log_dir_path of the dir were the logs to be trimmed are to be found and run this file.
(Tested with python38)

Ideas:
    - Sometimes one is printing the callstack of every callable in the callstack of the most stackfull. In such case it
    would be interesting to compress all that into one call stack, e.g. This makes sense in combination with STACK

    Untrimmed:
    callerOfCaller
    callerOfCalled <- callerOfCaller
    called <- callerOfCalled <- callerOfCaller

    Trimmed:
    called <- callerOfCalled <- callerOfCaller

    - Sometimes callstack repeats itself, spectially if multiple objects are initialized in the same way, maybe tis
    worth it to compress this, however more field experience is needed to know hoe common this actually is, although
    maybe some general rule of compression can be applied

    - Sometimes its not that one line of the log repeats, but that a bunch of lines repeat, like a group of three or
    four, they should also be compressed

"""

import re
from pathlib import Path
from time import time

start_time = time()

log_dir_path = Path(r'C:\trunk2\game\bin\client\.on_discon_bug_logs')
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
