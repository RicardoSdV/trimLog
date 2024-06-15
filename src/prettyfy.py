from typing import List

from src.compress import CompressionFormatList
from src.constants import INDENT_STR


def prettyfy_lines(cfl: CompressionFormatList, depth: int = 0) -> List[str]:
    cnt = cfl.cnt
    indent = depth * INDENT_STR
    result = []

    if cnt > 1:
        result.append(f'{(depth-1) * INDENT_STR}{cnt}x\n')

    for line in cfl:
        if isinstance(line, CompressionFormatList):
            result.extend(prettyfy_lines(line, depth + 1))
        elif isinstance(line, str):
            result.append(f'{indent}{line}')
        else:
            raise TypeError('Wrong type in compressed list: type(line)', type(line))
    return result
