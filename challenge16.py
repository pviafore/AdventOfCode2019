from functools import cache
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
    return [calculate_fft_digit(index, signal) for index in range(len(signal))]

def calculate_fft_digit(index: int, signal: List[int]) -> int:
    pattern = calculate_cycled_pattern(index)
    return abs(sum(starmap(mul, zip(pattern, signal)))) % 10


def calculate_cycled_pattern(index: int) -> Iterator[int]:
    pattern = cycle(chain.from_iterable(calculate_pattern(index+1)))
    next(pattern)
    return pattern

@cache
def calculate_pattern(index: int) -> list[list[int]]:
    base_pattern = [0, 1, 0, -1]
    full_pattern = [[n] * index for n in base_pattern]
    return full_pattern


def get_digit_at(position: int) -> list[int]:
    pattern_index = position - ( position // len(SIGNAL) * len(SIGNAL)) - 1
    return SIGNAL[pattern_index]

def get_fft_extended(phases: int) -> str:
    offset = int("".join(str(i) for i in SIGNAL[:7]))+1
    print(offset)
    numbers = [get_digit_at(n) for n in range(offset, len(SIGNAL)*10000)]
    for phase in range(phases):
        print(f"PHASE {phase}")
        total_numbers = sum(numbers)
        new_numbers = []
        for index in range(len(numbers)):
            new_numbers.append(total_numbers % 10)
            total_numbers -= numbers[index]
        numbers = new_numbers
    return "".join(str(n) for n in numbers[:8])

SIGNAL = get_signal()
if __name__ == "__main__":
    print(get_fft_digits(SIGNAL, 100))
    print(get_fft_extended(100))
