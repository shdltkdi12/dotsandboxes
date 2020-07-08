'''
    Creators: Andrew Kinchler
    Date: 11/19/2019

    This is the file to implement our Minimax algorithm
'''

import copy
import random


class Node(object):
    def __init__(self, player_input, depth_input, boxes_input, walls_input, cords_input=None, value_input=0):
        if cords_input is None:
            cords_input = []
        self.player = player_input
        self.depth = depth_input
        self.boxes = boxes_input
        self.walls = walls_input
        self.cords = cords_input
        self.value = value_input
        self.children = []
        self.create_children()

    def create_children(self):
        if _no_more_moves(self.walls) or self.depth <= 0:
            self.value = _calculate_score(self.boxes)
        else:
            for column in range(len(self.walls)):
                for row in range(len(self.boxes)):
                    if not self.walls[column][row]:
                        child_boxes = copy.copy(self.boxes)
                        child_walls = copy.copy(self.walls)
                        child_walls[column][row] = True
                        child_cords = [column, row]
                        child_boxes, get_another_turn = _set_all_slots(child_boxes, child_walls, self.player)

                        if get_another_turn:
                            self.children.append(Node(self.player, self.depth - 1, child_boxes,
                                                      child_walls, child_cords))
                        else:
                            if self.player == 'A':
                                self.children.append(Node('B', self.depth - 1, child_boxes, child_walls, child_cords))
                            elif self.player == 'B':
                                self.children.append(Node('A', self.depth - 1, child_boxes, child_walls, child_cords))
                            else:
                                exit("Node had unexpected player value")


def min_max(node):
    if node.depth == 0 or not node.children:
        return node.value, node.cords

    best_value = 1000
    best_cords = []
    is_player_a = False
    if node.player == 'A':
        best_value = -1000
        is_player_a = True

    for child in node.children:
        value, cords = min_max(child)
        if is_player_a:
            if value > best_value or (value == best_value and random.randint(1, 10) > 5):
                best_value = value
                best_cords = child.cords
        else:
            if value < best_value or (value == best_value and random.randint(1, 10) > 5):
                best_value = value
                best_cords = child.cords

    return best_value, best_cords


def _no_more_moves(walls):
    for column_list in range(0, len(walls)):
        if False in walls[column_list]:
            return False
    return True


def _set_all_slots(boxes, walls, player):
    get_another_turn = False

    for column in range(len(boxes)):
        for row in range(len(boxes)):
            if boxes[column][row] != 0 or _get_number_of_walls(boxes, walls, column, row) < 4:
                continue

            get_another_turn = True
            if player == 'A':
                boxes[column][row] = 1
            elif player == 'B':
                boxes[column][row] = 2
            else:
                boxes[column][row] = 3

    return boxes, get_another_turn


def _get_number_of_walls(boxes, walls, slot_column, slot_row):
    number_of_walls = 0

    # if right wall is set
    if slot_column == len(boxes) - 1:
        number_of_walls += 1
    elif walls[(slot_column * 2) + 2][slot_row]:
        number_of_walls += 1

    # if lower wall is set
    if slot_row == len(boxes) - 1:
        number_of_walls += 1
    elif walls[(slot_column * 2) + 1][slot_row + 1]:
        number_of_walls += 1

    # if left wall is set
    if walls[slot_column * 2][slot_row]:
        number_of_walls += 1

    # if upper wall is set
    if walls[(slot_column * 2) + 1][slot_row]:
        number_of_walls += 1

    return number_of_walls


def _calculate_score(boxes):
    player_a = 0
    player_b = 0

    for column in range(len(boxes)):
        for row in range(len(boxes)):
            if boxes[column][row] == 1:
                player_a += 1
            elif boxes[column][row] == 2:
                player_b += 1

    return player_a - player_b
