from math import gcd
from typing import List, Tuple

from common.input_handling import get_input


def get_instructions() -> List[str]:
    return get_input("input/input22.txt")

def get_additive_and_factor(instructions: List[str], num_cards: int) -> Tuple[int, int]:
    total = 0
    multiplication = 1
    for instruction in instructions:
        if instruction == "deal into new stack":
            multiplication *= -1
            total = -total + (num_cards - 1)
        elif instruction.startswith("cut"):
            _, num = instruction.split(' ')
            total -= int(num)
        elif instruction.startswith("deal"):
            *_words, num = instruction.split(' ')
            total *= int(num)
            multiplication *= int(num)
        else:
            raise RuntimeError("Unknown instruction")
    return multiplication, total

def get_inverse_additive_and_factor(instructions: List[str], num_cards: int) -> Tuple[int, int]:
    total = 0
    multiplication = 1
    for instruction in instructions[::-1]:
        if instruction == "deal into new stack":
            multiplication *= -1
            total = -total + (num_cards - 1)
        elif instruction.startswith("cut"):
            _, num = instruction.split(' ')
            total += int(num)
        elif instruction.startswith("deal"):
            *_words, num = instruction.split(' ')
            total *= mod_inverse(int(num), num_cards)
            multiplication *= mod_inverse(int(num), num_cards)
        else:
            raise RuntimeError("Unknown instruction")
    return multiplication, total

def get_card_index(instructions: List[str], value: int, num_cards: int) -> int:
    factor, additive = get_additive_and_factor(instructions, num_cards)
    return (value*factor + additive) % num_cards

def mod_inverse(value: int, modulo: int) -> int:
    result = gcd(value, modulo)
    if  result != 1:
        raise RuntimeError("Inverse doesn't exist")

    return pow(value, modulo - 2, modulo)

def get_card_index_after_big_shuffle(instructions: List[str]):
    card_index = 2020
    num_cards = 119315717514047
    factor, additive = get_inverse_additive_and_factor(instructions, num_cards)
    times = 101741582076661
    return (pow(factor, times, num_cards) * card_index +
            additive * (pow(factor, times, num_cards) - 1) *
            mod_inverse(factor - 1 + num_cards, num_cards)) % num_cards



INSTRUCTIONS = get_instructions()
if __name__ == "__main__":
    print(get_card_index(INSTRUCTIONS, 2019, 10007))
    print(get_card_index_after_big_shuffle(INSTRUCTIONS))
