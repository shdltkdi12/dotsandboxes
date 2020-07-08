import pygame
import numpy as np
import sys
import minimax
import otherAlgorithms
import copy
import random
import time


class Game:
    def __init__(self):
        self.grid_size = 10  # default
        if len(sys.argv) > 1:
            self.grid_size = int(sys.argv[1])

        # It turns out that there are nice structures when setting ~0.75 walls per slot
        self.start_walls = int(0.75 * self.grid_size ** 2)

        self.accept_clicks = True
        # variables for the boxes for each player (x would be computer)
        self.a_boxes = 0
        self.b_boxes = 0
        self.x_boxes = 0

        self.turn = "X"
        self.caption = "'s turn    "

        # 0 empty 1 is A 2 is B and 3 is X
        self.boxes = np.zeros((self.grid_size, self.grid_size), np.int)
        self.walls = np.zeros((self.grid_size * 2, self.grid_size), np.dtype(bool))

        for column in range(self.grid_size * 2):
            for row in range(self.grid_size):
                if column == 0 or (column % 2 == 1 and row == 0):
                    self.walls[column][row] = True

        # initialize pygame
        pygame.init()

        # set the display size (one slot has 30x30 pixels; Walls: 4x26 Box: 26x26)
        self.screen = pygame.display.set_mode([30 * self.grid_size + 4, 30 * self.grid_size + 4])

        # load all images
        self.empty = pygame.image.load("pics/empty.png")
        self.A = pygame.image.load("pics/A.png")
        self.B = pygame.image.load("pics/B.png")
        self.X = pygame.image.load("pics/X.png")
        self.block = pygame.image.load("pics/block.png")
        self.line_x = pygame.image.load("pics/lineX.png")
        self.line_x_empty = pygame.image.load("pics/lineXempty.png")
        self.line_y = pygame.image.load("pics/lineY.png")
        self.line_y_empty = pygame.image.load("pics/lineYempty.png")

        # now it's the first players turn
        self.turn = 'A'
        self.show()

        self.max_depth = 2
        self.total_turns = 0
        self.turns = 0
        self.all_turn_times = []
        self.my_box = [-100, -100]

        while True:
            self.total_turns += 1
            column = 0
            row = 0
            # Our Minimax's Turn
            if self.turn == 'A':
                self.turns += 1
                boxes_copy = copy.copy(self.boxes)
                walls_copy = copy.copy(self.walls)
                start = time.time()
                node = minimax.Node('A', self.max_depth, boxes_copy, walls_copy)
                best_value, best_cords = minimax.min_max(node)
                turn_time = time.time() - start
                self.all_turn_times.append(turn_time)
                column = best_cords[0]
                row = best_cords[1]

            # Other Algorithm's turn (Random right now)
            if self.turn == 'B':
                # Just uncomment one at a time to get it to play against the minimax algorithm
                # cords = otherAlgorithms.defensive_algorithm(self.walls, self.boxes)
                # cords, self.my_box = otherAlgorithms.pick_randomly(self.walls, self.boxes, self.my_box)
                cords = otherAlgorithms.pick_randomly(self.walls, self.grid_size)
                column = cords[0]
                row = cords[1]

            self.walls[column][row] = True

            # the rest is used by both comps
            if column % 2 == 0:
                is_horizontal_wall = False
            else:
                is_horizontal_wall = True

            column = int(column / 2)

            if is_horizontal_wall:
                self.screen.blit(self.line_x, (column * 30 + 4, row * 30))
            else:
                self.screen.blit(self.line_y, (column * 30, row * 30 + 4))

            if not self.set_all_slots() > 0:
                if self.turn == "A":
                    self.turn = "B"
                elif self.turn == "B":
                    self.turn = "A"

            if self.won():
                print('Total Turns = ', self.total_turns)
                print('Minimax Turns = ', self.turns)
                total_time = 0
                for round_trip in self.all_turn_times:
                    total_time += round_trip
                average_time = total_time / len(self.all_turn_times)
                print('Depth searched = ', self.max_depth)
                print('Average Turn Time = ', '{0:.3f}'.format(round(average_time, 3)))
                print('Maximum Turn Time = ', '{0:.3f}'.format(round(max(self.all_turn_times), 3)))
                print('Total Minimax Time = ', '{0:.3f}'.format(round(total_time, 3)))
                while True:
                    for event1 in pygame.event.get():
                        if event1.type == pygame.QUIT:
                            pygame.quit()
                            exit(0)
            else:
                #time.sleep(1)
                # set the display caption
                pygame.display.set_caption(self.turn + self.caption + "     A:" + str(
                    self.a_boxes) + "   B:" + str(self.b_boxes))

                # update the players screen
                pygame.display.flip()

    def get_number_of_walls(self, slot_column, slot_row):
        """
        Get the number of set walls around the passed slot
        :param slot_column: x of the slot
        :param slot_row: y of the slot
        :return: number of set walls
        """
        number_of_walls = 0

        if slot_column == self.grid_size - 1:
            number_of_walls += 1
        elif self.walls[(slot_column * 2) + 2][slot_row]:
            number_of_walls += 1

        if slot_row == self.grid_size - 1:
            number_of_walls += 1
        elif self.walls[(slot_column * 2) + 1][slot_row + 1]:
            number_of_walls += 1

        if self.walls[slot_column * 2][slot_row]:
            number_of_walls += 1

        if self.walls[(slot_column * 2) + 1][slot_row]:
            number_of_walls += 1

        return number_of_walls

    def set_all_slots(self):
        """
        Find all newly closed boxes and close them for the current player
        :return: number of closed boxes
        """
        to_return = 0

        for column in range(self.grid_size):
            for row in range(self.grid_size):
                if self.boxes[column][row] != 0 or self.get_number_of_walls(column, row) < 4:
                    continue

                if self.turn == "A":
                    self.boxes[column][row] = 1
                    self.screen.blit(self.A, (column * 30 + 4, row * 30 + 4))
                    self.a_boxes += 1
                elif self.turn == "B":
                    self.boxes[column][row] = 2
                    self.screen.blit(self.B, (column * 30 + 4, row * 30 + 4))
                    self.b_boxes += 1
                elif self.turn == "X":
                    self.boxes[column][row] = 3
                    self.screen.blit(self.X, (column * 30 + 4, row * 30 + 4))
                    self.x_boxes += 1

                to_return += 1

        return to_return

    def won(self):
        """
        Check whether the game was finished
        If so change the caption to display the winner
        :return: won or not
        """
        if self.a_boxes + self.b_boxes + self.x_boxes == self.grid_size ** 2:
            if self.a_boxes < self.b_boxes:
                won_caption = "Player B won!   Congrats"
            elif self.b_boxes < self.a_boxes:
                won_caption = "Player A won!   Congrats"
            else:
                won_caption = "It's a tie!"

            # set the display caption
            pygame.display.set_caption(won_caption)

            # update the players screen
            pygame.display.flip()

            return True
        else:
            return False

    def show(self):
        """
        Reload the screen
        Use the current grid and wall information to
        update the players screen
        """
        self.screen.fill(0)

        # loop over all slots
        for column in range(self.grid_size * 2):
            for row in range(self.grid_size):
                x = int(column / 2) * 30
                y = row * 30

                if column % 2 == 0:
                    y += 4
                    if not self.walls[column][row]:
                        self.screen.blit(self.line_y_empty, (x, y))
                    else:
                        self.screen.blit(self.line_y, (x, y))

                if column % 2 == 1:
                    self.screen.blit(self.block, (x, y))
                    x += 4
                    if not self.walls[column][row]:
                        self.screen.blit(self.line_x_empty, (x, y))
                    else:
                        self.screen.blit(self.line_x, (x, y))

                    y += 4
                    box_column = int(column / 2)
                    if self.boxes[box_column][row] == 0:
                        self.screen.blit(self.empty, (x, y))
                    elif self.boxes[box_column][row] == 1:
                        self.screen.blit(self.A, (x, y))
                    elif self.boxes[box_column][row] == 2:
                        self.screen.blit(self.B, (x, y))
                    elif self.boxes[box_column][row] == 3:
                        self.screen.blit(self.X, (x, y))

        pygame.display.set_caption(self.turn + self.caption + "     A:" + str(self.a_boxes) + "   B:"
                                   + str(self.b_boxes))
        pygame.display.flip()


game = Game()  # start a game
