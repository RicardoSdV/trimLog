from typing import Union


class CompressionFormatList(list):
    def __init__(self, *args, cnt: int = 1, rep: str = '') -> None:
        super().__init__(*args)
        self.cnt = cnt
        self.rep = rep

    def __eq__(self, other: Union['CompressionFormatList', str]) -> bool:
        if isinstance(other, CompressionFormatList):
            return super().__eq__(other) and self.cnt == other.cnt and self.rep == other.rep
        return False



CompressionRecursive = CompressionFormatList[str, CompressionFormatList]