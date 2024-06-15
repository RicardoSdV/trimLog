from src.compress import compress, remove_redundant, CompressionFormatList
from src.format import remove_datetime_and_log_type_prefixes_from_lines_in_place, format_lines_for_lines_compression
from src.path_ops import find_read_and_write_log_paths
from src.prettyfy import prettyfy_lines


def run(
        force_retrim: bool = True,
        log_dir_path: str = r'C:\prjs\trimLog\logs_dir_example'
):

    log_paths = find_read_and_write_log_paths(force_retrim, log_dir_path)

    for read_path, write_path in log_paths:

        print('read_path, write_path', read_path, write_path)

        with open(read_path, 'r') as file:
            lines = file.readlines()
        if len(lines) < 1: continue


        remove_datetime_and_log_type_prefixes_from_lines_in_place(lines)


        cfl_lines = format_lines_for_lines_compression(lines)


        cfl_lines = compress(cfl_lines)
        print(cfl_lines)


        cfl_lines = remove_redundant(cfl_lines, CompressionFormatList(cnt=1, rep='lines'))


        pretty_lines = prettyfy_lines(cfl_lines)


        with open(write_path, 'w') as f:
            f.writelines(pretty_lines)


run()
