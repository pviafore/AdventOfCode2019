

def test_day1():
    from challenge1 import get_total_fuel, MASSES, get_total_additional_fuel
    assert get_total_fuel(MASSES) == 3397667
    assert get_total_additional_fuel(MASSES) == 5093620

def test_day2():
    from challenge2 import get_value_at_address_zero_after_calculation, get_correct_noun_verb
    assert get_value_at_address_zero_after_calculation() == 5866663
    assert get_correct_noun_verb() == 4259

def test_day3():
    from challenge3 import WIRES, get_distance_to_closest_intersection, get_minimal_timing_delay
    assert get_distance_to_closest_intersection(WIRES) == 1285
    assert get_minimal_timing_delay(WIRES) == 14228

def test_day4():
    from challenge4 import PASSWORDS, get_number_of_matching_passwords, get_number_of_strict_matching_passwords
    assert get_number_of_matching_passwords(PASSWORDS) == 1650
    assert get_number_of_strict_matching_passwords(PASSWORDS) == 1129
