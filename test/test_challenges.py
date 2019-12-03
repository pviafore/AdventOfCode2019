

def test_day1():
    from challenge1 import get_total_fuel, MASSES, get_total_additional_fuel
    assert get_total_fuel(MASSES) == 3397667
    assert get_total_additional_fuel(MASSES) == 5093620

def test_day2():
    from challenge2 import get_value_at_address_zero_after_calculation, get_correct_noun_verb
    assert get_value_at_address_zero_after_calculation() == 5866663
    assert get_correct_noun_verb() == 4259
