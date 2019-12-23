

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

def test_day5():
    from challenge5 import run_program 
    assert run_program(1) == 9219874
    assert run_program(5)== 5893654

def test_day6():
    from challenge6 import ORBITS, get_total_orbits, get_transfer_distance
    assert get_total_orbits(ORBITS) == 142497
    assert get_transfer_distance(ORBITS) == 301

def test_day7():
    from challenge7 import find_maximum_signal_to_thrusters, find_maximum_signal_to_thrusters_with_feedback 
    assert find_maximum_signal_to_thrusters() == 359142
    assert find_maximum_signal_to_thrusters_with_feedback() == 4374895

def test_day8():
    from challenge8 import IMAGE_DATA, get_product_of_1s_and_2s_in_target_layer
    assert get_product_of_1s_and_2s_in_target_layer(IMAGE_DATA) == 2356

def test_day9():
    from challenge9 import run_program
    assert run_program(1) == 2955820355
    assert run_program(2) == 46643

def test_day10():
    from challenge10 import ASTEROIDS, get_200th_asteroid_destroyed, get_number_of_asteroids_seen_from_best_station
    assert get_number_of_asteroids_seen_from_best_station(ASTEROIDS) == 280
    assert get_200th_asteroid_destroyed(ASTEROIDS) == 706

def test_day11():
    from challenge11 import Color, run_program
    assert run_program(Color.BLACK).get_painted_squares() == 1907

def test_day12():
    from challenge12 import MOONS, run_simulation, run_simulation_until_back_to_initial
    assert run_simulation(1000, MOONS) == 6735
    assert run_simulation_until_back_to_initial(MOONS) ==  326489627728984

def test_day13():
    from challenge13 import run_program
    assert run_program().get_number_of_blocks() == 376
    assert run_program(2).get_score() == 18509

def test_day14():
    from challenge14 import REACTIONS, get_number_of_ore, find_number_of_fuel
    assert get_number_of_ore(REACTIONS) == 751038
    assert find_number_of_fuel(REACTIONS) == 2074843

def test_day15():
    from challenge15 import run_program
    assert run_program().get_distance_to_oxygen_station() == 404
    assert run_program().calculate_distance_for_oxygen_to_progpagate() == 406

def test_day16():
    from challenge16 import SIGNAL, get_fft_digits
    assert get_fft_digits(SIGNAL, 100) == str(50053207)

def test_day17():
    from challenge17 import run_program
    assert run_program() == 7720

def test_day22():
    from challenge22 import INSTRUCTIONS, get_card_index_after_big_shuffle, get_card_index
    assert get_card_index(INSTRUCTIONS, 2019, 10007) == 6638
    assert get_card_index_after_big_shuffle(INSTRUCTIONS) == 77863024474406
