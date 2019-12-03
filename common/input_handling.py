from typing import Any, Callable, List

TransformFunc = Callable[[str], Any]

def get_input(filename: str, func: TransformFunc = str, *, delimiter: str = '\n') -> List[Any]:
    with open(filename) as input_file:
        return [func(l) for l in input_file.read().split(delimiter) if l]
