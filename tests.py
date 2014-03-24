import unittest
from board import *
from save import *
from pickle import dumps


class BoardTests(unittest.TestCase):
    def test_snake_turns_properly(self):
        s = Snake(10, 10)
        s.turn(directions['down'])
        self.assertEqual(s.direction, directions['down'])

        s.turn(directions['up'])
        self.assertEqual(s.direction, directions['down'])

    def test_new_head_works(self):
        s = Snake(3, 3)
        self.assertEqual(s.new_head(), (3, 4))

    def test_snake_steps_properly(self):
        s = Snake(5, 5)
        s.step(eaten=False)
        self.assertEqual(s.head(), (5, 6))
        self.assertEqual(s.tail(), (5, 4))

        s.step(eaten=True)
        self.assertEqual(s.tail(), (5, 4))

    def test_snake_dies_when_a_wall_is_hit(self):
        b = Board(level_difficulty=5, random_levels=False)
        b.snake.body = [(2, 1), (1, 1)]
        b.snake.direction = directions['up']

        self.assertRaises(Exception, Board.step, b)

    def test_save_load_work(self):
        board1 = Board(level_difficulty=5, random_levels=False)
        save('test_file', board1)
        board2 = load('test_file')

        self.assertEqual(pickle.dumps(board1), pickle.dumps(board2))

        self.assertIsNone(load('no_such_file_i_hope_:)'))


if __name__ == "__main__":
    unittest.main()
