from itertools import permutations
from queue import Queue
from threading import Thread
from typing import List, Tuple

from common.input_handling import get_input
from common.intcode_computer import Computer

def load_instructions() -> List[int]:
    return get_input("input/input7.txt", int, delimiter=",")

def find_maximum_signal_to_thrusters() -> int:
    return max(get_signal_for_thrusters(combo) for combo in permutations(range(5)))

def get_signal_for_thrusters(combo: Tuple[int, ...]) -> int:
    instructions = load_instructions()
    amplifiers = [Computer(instructions, quiet=True) for _ in range(len(combo))]
    amplifier_output = 0
    for amplifier, phase in zip(amplifiers, combo):
        run_amplifier(amplifier, phase, amplifier_output)
        amplifier_output = amplifier.get_last_output()
    return amplifier_output

def run_amplifier(amplifier: Computer, *initial_input: int):
    amplifier.inject_input(*initial_input)
    if amplifier.name == "A0":
        amplifier.inject_input(0)
    amplifier.run_loop()

def find_maximum_signal_to_thrusters_with_feedback() -> int:
    return max(get_signal_for_thrusters_feedback(combo) for combo in permutations(range(5, 10)))

def get_signal_for_thrusters_feedback(combo: Tuple[int, ...]) -> int:
    instructions = load_instructions()
    amplifiers = [Computer(instructions, quiet=True, name=f"A{i}") for i in range(len(combo))]
    setup_amplifiers_for_feedback(amplifiers)
    for amplifier, phase in zip(amplifiers, combo):
        thr = Thread(target=run_amplifier, args=(amplifier, phase))
        thr.start()
    thr.join()

    return amplifiers[-1].get_last_output()

def setup_amplifiers_for_feedback(amplifiers: List[Computer]):
    for amp in range(len(amplifiers) - 1):
        setup_communication(amplifiers[amp], amplifiers[amp + 1])
    setup_communication(amplifiers[-1], amplifiers[0])

def setup_communication(amplifier1: Computer, amplifier2: Computer):
    queue: Queue = Queue()
    amplifier1.output_function = lambda x: queue.put(int(x))
    amplifier2.input_function = queue.get


if __name__ == "__main__":
    print(find_maximum_signal_to_thrusters())
    print(find_maximum_signal_to_thrusters_with_feedback())
