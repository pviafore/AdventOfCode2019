from itertools import chain, cycle, starmap
from operator import mul
from typing import Iterator, List

from common.input_handling import get_input

def to_signal(text: str) -> List[int]:
    return [int(s) for s in text]

def get_signal() -> List[int]:
    return get_input("input/input16.txt", to_signal)[0]

def get_fft_digits(signal: List[int], number_of_phases: int) -> str:
    for _phase in range(number_of_phases):
        signal = fft(signal)
    return "".join(str(i) for i in signal[:8])

def fft(signal: List[int]) -> List[int]:
    return [calculate_fft_digit(index, signal) for index in range(1, len(signal) + 1)]

def calculate_fft_digit(index: int, signal: List[int]) -> int:
    pattern = calculate_pattern(index)
    return abs(sum(starmap(mul, zip(pattern, signal)))) % 10

def calculate_pattern(index: int) -> Iterator[int]:
    base_pattern = [0, 1, 0, -1]
    pattern = cycle(chain.from_iterable([n] * index for n in base_pattern))
    # exhaust first element
    next(pattern)
    return pattern


SIGNAL = get_signal()
if __name__ == "__main__":
    print(get_fft_digits(SIGNAL, 100))
    print(get_fft_digits(SIGNAL*10000, 100))
