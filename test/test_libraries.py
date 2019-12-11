from common.cartesian import Point, get_manhattan_distance, get_slope, ORIGIN, TextGrid

def test_manhattan_distance_on_self():
    assert get_manhattan_distance(Point(0,0), Point(0,0)) == 0

def test_manhattan_distance_on_distant_point():
    assert get_manhattan_distance(Point(0,0), Point(3,4)) == 7

def test_manhattan_distance_on_negative_point():
    assert get_manhattan_distance(Point(-1,-1), Point(3,4)) == 9

def test_point_to_right():
    assert Point(0,0).to_right() == Point(1,0)

def test_point_to_left():
    assert Point(0,0).to_left() == Point(-1,0)

def test_point_to_above():
    assert Point(0,0).to_above() == Point(0,1)

def test_point_to_below():
    assert Point(0,0).to_below() == Point(0,-1)

def test_text_grid_can_get_points():
    text_grid = TextGrid(["a", "b"])
    assert text_grid.get_all_points() == {Point(0, 0): "a", Point(0,1): "b"}

def test_text_grid_can_get_points_matching_symbol():
    text_grid = TextGrid(["ab", "bb"])
    assert sorted(text_grid.get_all_points_matching_symbol("b")) == [Point(0, 1), Point(1, 0), Point(1, 1)] 

def test_get_slope():
    assert get_slope(ORIGIN, Point(2,3)) == 3/2
    assert get_slope(Point(3,4), Point(2,3)) == 1 
    assert get_slope(Point(4,2), Point(4,0)) == float("-inf")
    assert get_slope(Point(4,2), Point(4,4)) == float("inf")
