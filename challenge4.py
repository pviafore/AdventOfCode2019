import re
from typing import List


def is_increasing(text: str) -> bool:
    return text == "".join(sorted(text))

def matches_pattern(text: str) -> bool:
    return re.search(r'(\d)\1', text) is not None

def get_number_of_matching_passwords(passwords: List[str]) -> int:
    return len([p for p in passwords if is_increasing(p) and matches_pattern(p)])

def matches_strict_pattern(text: str) -> bool:
    return any(len(m.group(0)) == 2 for m in re.finditer(r'(\d)\1+', text))

def get_number_of_strict_matching_passwords(passwords: List[str]) -> int:
    return len([p for p in passwords if is_increasing(p) and matches_strict_pattern(p)])

PASSWORDS = list(str(i) for i in range(178416, 676462))
if __name__ == "__main__":
    print(get_number_of_matching_passwords(PASSWORDS))
    print(get_number_of_strict_matching_passwords(PASSWORDS))
