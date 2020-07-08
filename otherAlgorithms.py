'''
    Creators: Andrew Kinchler
    Date: 11/19/2019

    This is the file to implement other base algorithms to test against
'''

import random


def pick_randomly(walls, grid_size):
    searching_for_open_wall = True
    while searching_for_open_wall:
        column = random.randint(1, (grid_size * 2) - 1)
        row = random.randint(0, grid_size - 1)

        if not walls[column][row]:
            searching_for_open_wall = False
    cords = [column, row]
    return cords


def greedy_algorithm(walls, boxes, my_box):
    if my_box == [-100, -100] or _get_number_of_open_walls(boxes, walls, my_box[0], my_box[1]) == 0:
        my_box = _get_new_box(boxes, walls)
    column = my_box[0]
    row = my_box[1]
    cords = _find_open_wall(boxes, walls, column, row)
    return cords, my_box


def mirror_algorithm(walls, grid_size):
    pass


def defensive_algorithm(walls, boxes):
    box_cords = _find_most_open_box(boxes, walls)
    column = box_cords[0]
    row = box_cords[1]
    return _find_open_wall(boxes, walls, column, row)


def _find_open_wall(boxes, walls, column, row):
    not_found = True
    while not_found:
        number = random.randint(0, 3)
        # if right wall isn't set
        if number == 0 and not column == len(boxes) - 1:
            if not walls[column * 2 + 2][row]:
                cords = [column * 2 + 2, row]
                not_found = False
        # if lower wall isn't set
        if number == 1 and not row == len(boxes) - 1:
            if not walls[column * 2 + 1][row + 1]:
                cords = [column * 2 + 1, row + 1]
                not_found = False
        # if left wall isn't set
        if number == 2 and not walls[column * 2][row]:
            cords = [column * 2, row]
            not_found = False
        # if upper wall isn't set
        if number == 3 and not walls[column * 2 + 1][row]:
            cords = [column * 2 + 1, row]
            not_found = False
    return cords


def _find_most_open_box(boxes, walls):
    most_open_walls = -100
    most_open_box = []
    for column in range(len(boxes)):
        for row in range(len(boxes)):
            box_walls = _get_number_of_open_walls(boxes, walls, column, row)
            if box_walls == 1:
                most_open_box = [column, row]
                return most_open_box
            elif box_walls > most_open_walls or (box_walls == most_open_box and random.randint(1, 10) > 5):
                most_open_walls = box_walls
                most_open_box = [column, row]
    return most_open_box


def _get_number_of_open_walls(boxes, walls, slot_column, slot_row):
    number_of_open_walls = 4

    # if right wall is set
    if slot_column == len(boxes) - 1:
        number_of_open_walls -= 1
    elif walls[(slot_column * 2) + 2][slot_row]:
        number_of_open_walls -= 1

    # if lower wall is set
    if slot_row == len(boxes) - 1:
        number_of_open_walls -= 1
    elif walls[(slot_column * 2) + 1][slot_row + 1]:
        number_of_open_walls -= 1

    # if left wall is set
    if walls[slot_column * 2][slot_row]:
        number_of_open_walls -= 1

    # if upper wall is set
    if walls[(slot_column * 2) + 1][slot_row]:
        number_of_open_walls -= 1

    return number_of_open_walls


def _get_new_box(boxes, walls):
    no_box_yet = True
    best_box_walls = 100
    my_box = None
    for column in range(len(boxes)):
        for row in range(len(boxes)):
            box_walls = _get_number_of_open_walls(boxes, walls, column, row)
            if box_walls > 0:
                if no_box_yet:
                    no_box_yet = False
                    my_box = [column, row]
                    best_box_walls = box_walls
                if box_walls == 1:
                    my_box = [column, row]
                    return my_box
                elif random.randint(1, 10) > 7:
                    my_box = [column, row]
    return my_box
