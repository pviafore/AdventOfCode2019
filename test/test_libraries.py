from common.cartesian import Point, get_manhattan_distance

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
