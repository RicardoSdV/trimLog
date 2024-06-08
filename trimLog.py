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

    - Sometimes callstack repeats itself, specially if multiple objects are initialized in the same way, maybe tis
    worth it to compress this, however more field experience is needed to know hoe common this actually is, although
    maybe some general rule of compression can be applied

"""

import re
from pathlib import Path
from time import time

start_time = time()

log_dir_path = Path(r'C:\prjs\trimLog\logs_dir_example')
log_paths = log_dir_path.glob('**/*.log')

force_retrim = False

for log_path in log_paths:

    """ ======================= INIT STUFF ======================= """

    if log_path.name.startswith('t_'): continue

    trimmed_log_path = log_path.with_name('t_' + log_path.name)
    if trimmed_log_path.exists() and not force_retrim: continue

    with open(log_path, 'r') as f:
        lines = f.readlines()

    if len(lines) < 1: continue

    """ =========================================================== """

    """ ======================= REMOVING PREFIXES ======================= """

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

    """ ================================================================== """

    """ =================== Compressing with multiple passes when a group of lines repeats ========================= """

    post_pass_lines = lines; max_group_size = 100  # inclusive
    for group_size in range(1, max_group_size + 1):
        pre_pass_lines = post_pass_lines; post_pass_lines = []
        prev_group = pre_pass_lines[0: group_size]; cnt = 1
        for i in range(group_size, len(pre_pass_lines) + group_size, group_size):
            group = pre_pass_lines[i: i+group_size]
            if group == prev_group: cnt += 1
            else:
                if cnt > 1:
                    if group_size > 1: post_pass_lines.extend([f'{cnt}x\n'] + [f'    {line}' for line in prev_group])
                    else: post_pass_lines.append(f'{cnt}x {prev_group[0]}')
                else: post_pass_lines.extend(prev_group)
                cnt = 1; prev_group = group
    lines = post_pass_lines

    """=============================================================================================================="""

    """ ============= Compressing with multiple passes when a group of frames in the call stack repeats ============ """
    post_pass_lines = []
    for line in lines:
        if ' <- ' not in line:
            post_pass_lines.append(line)
            continue

        line = line.strip()

        nums = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
        chars = []
        starts_with_num, followed_by_x, followed_by_space = False, False, False
        for char in line:
            if char in nums and not followed_by_x and not followed_by_space:
                starts_with_num = True
                chars.append(char)
            elif starts_with_num and char == 'x' and not followed_by_x and not followed_by_space:
                followed_by_x = True
                chars.append(char)
            elif followed_by_x and char == ' ' and not followed_by_space:
                followed_by_space = True
                chars.append(char)
            else:
                break

        if starts_with_num and followed_by_x and followed_by_space:
            repeats_marker = ''.join(chars)
            line = line[len(repeats_marker):]
        else:
            repeats_marker = ''

        frames = line.split(' <- ')

        pre_pass_frames = None
        post_pass_frames = frames
        for group_size in range(1, max_group_size + 1):
            pre_pass_frames = post_pass_frames; post_pass_frames = []

            prev_group = pre_pass_frames[0: group_size]; cnt = 1
            for i in range(group_size, len(pre_pass_frames) + group_size, group_size):
                group = pre_pass_frames[i: i + group_size]
                if group == prev_group: cnt += 1
                else:
                    if cnt > 1:
                        post_pass_frames.append(f'{cnt}x[{" <- ".join(prev_group)}]')
                    else:
                        post_pass_frames.extend(prev_group)
                    cnt = 1; prev_group = group

        post_pass_lines.append(f'{repeats_marker}{" <- ".join(post_pass_frames)}\n')

    lines = post_pass_lines

    """ ============================================================================================================ """

    """ ======================= Save lines to new file ======================= """

    with open(trimmed_log_path, 'w') as f:
        f.writelines(lines)

    """ ======================================================================= """


print('Done trimming, took:', time() - start_time)
