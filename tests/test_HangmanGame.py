import io
from unittest import TestCase, main, mock
from hangman import HangmanGame


class TestGamePlay(TestCase):

    def setUp(self):
        """ Creates GamePlay class for all the unittests. """
        self.game_one = HangmanGame()
        self.game_two = HangmanGame()

    def test_is_valid_filename_NameError(self):
        with self.assertRaises(NameError, msg='NameError was not thrown when an incorrect filename was input'):
            HangmanGame(filename='word_bank')

    def test_read_file_stats_FileFoundError(self):
        with self.assertRaises(FileNotFoundError, msg='FileNotFoundError was not thrown when an incorrect '
                                                      'filename was input'):
            HangmanGame(filename='word_banker.txt')

    def test_is_comment_true(self):
        result = HangmanGame.is_comment('# This is a comment')
        self.assertEqual(True, result)

    def test_is_comment_false(self):
        result = HangmanGame.is_comment('This is a not comment')
        self.assertEqual(False, result)

    def test_set_word_empty(self):
        """ Checks if the word is set correctly. """
        self.game_one.set_word()
        self.assertIsNotNone(self.game_one.word, 'Variable \'word\' is empty')
        self.assertEqual(len(self.game_one.word_display), len(self.game_one.word), 'Length of \'word_display\' and '
                                                                                   '\'word\' do not match. ')
        self.assertIn('_', self.game_one.word_display, '\'word_display\' does not contain dashes: \'_\'')

    @mock.patch('builtins.input', lambda *args: 'n')
    def test_set_word_error_n(self):
        """ Checks if the correct error is raised. """
        self.game_one.word_bank = set()

        with self.assertRaises(UserWarning, msg='The word bank has been exhausted and you did not update it.'):
            with mock.patch('sys.stdout', new=io.StringIO()) as stdout:
                self.game_one.set_word()
                self.assertEqual('Error: The word bank has been exhausted. All the words have been used.\n',
                                 stdout.getvalue(),
                                 'UserWarning not raised')

    def test_set_word_error_y(self):
        """
        Checks if the correct error is raised.

        Notes: The syntax for this test is based on Pytest and not unittest.
        """
        self.game_one.word_bank = set()

        with mock.patch('builtins.input', side_effect=['y', 'word_bank.txt']):
            self.game_one.set_word()

        self.assertIsNotNone(self.game_one.word_bank, 'word_bank is not updated.')
        self.assertIsNotNone(self.game_one.word, 'Word is not updated after updating file.')

    def test_update_word_display(self):
        self.game_one.set_word()
        letter = self.game_one.word[1]
        self.game_one.update_word_display(letter)
        self.assertEqual(letter, self.game_one.word_display[1],
                         '\'word_display\' is not updated correctly. The second letter should be displayed.')

    def test_update_hangman_head(self):
        self.game_one.incorrect_guesses = ['a']
        self.game_one.update_hangman()
        self.assertEqual('O', self.game_one.hangman.get('head'), 'hangman\'s head was not updated.')

    def test_update_hangman_body(self):
        self.game_one.incorrect_guesses = ['a', 'b']
        self.game_one.update_hangman()
        self.assertEqual('|', self.game_one.hangman.get('body'), 'hangman\'s body was not updated.')

    def test_update_hangman_right_hand(self):
        self.game_one.incorrect_guesses = ['a', 'b', 'c']
        self.game_one.update_hangman()
        self.assertEqual('/', self.game_one.hangman.get('right_hand'), 'hangman\'s right_hand was not updated.')

    def test_update_hangman_left_hand(self):
        self.game_one.incorrect_guesses = ['a', 'b', 'c', 'd']
        self.game_one.update_hangman()
        self.assertEqual('\\', self.game_one.hangman.get('left_hand'), 'hangman\'s left_hand was not updated.')

    def test_get_status_guessing_hello(self):
        self.game_one.set_word()
        self.game_one.word = 'hello'
        self.assertEqual('guessing', self.game_one.get_status(), 'Initial state of the game is incorrect')

        self.game_one.word_display = ['o']
        self.assertEqual('guessing', self.game_one.get_status(), 'State of the game after one move is incorrect')

    def test_get_status_won_hello(self):
        self.game_one.set_word()
        self.game_one.word = 'hello'
        self.game_one.word_display = ['h', 'e', 'l', 'l', 'o']
        self.assertEqual('won', self.game_one.get_status(), 'State of a game won is incorrect')

    def test_get_status_guessing_world(self):
        self.game_two.set_word()
        self.game_two.word = 'world'
        self.assertEqual('guessing', self.game_two.get_status(), 'Initial state of the game is incorrect')

    def test_get_status_lost_world(self):
        self.game_two.set_word()
        self.game_two.word = 'world'
        self.game_two.word_display = ['w', 'o', 'r', 'l', '_']
        self.game_two.incorrect_guesses = ['i', 'p', 't', 'q', 's', 'n']
        self.assertEqual('lost', self.game_two.get_status(), 'State of a game lost is incorrect')

    def test_update_points_hello_right_3(self):
        self.game_one.word = 'hello'
        self.game_one.word_display = list('hello')
        self.game_one.incorrect_guesses = ['r', 'p', 'q']
        self.game_one.correct_guesses = ['h', 'e', 'l', 'o']
        points = self.game_one.update_points()
        self.assertEqual(7, points, f'Points for \'hello\' should be 7 and not {points}')

    def test_update_points_hello_wrong_2(self):
        self.game_one.word = 'hello'
        self.game_one.word_display = list('h___o')
        self.game_one.incorrect_guesses = ['r', 't', 'q', 'z', 'y', 'n']
        self.game_one.correct_guesses = ['h', 'o']
        points = self.game_one.update_points()
        self.assertEqual(-2, points, f'Points for \'h___o\' should be -2 and not {points}')

    def test_update_points_world_right(self):
        self.game_two.word = 'world'
        self.game_two.word_display = list('world')
        self.game_two.incorrect_guesses = ['i', 'p', 't', 'q', 's']
        self.game_two.correct_guesses = ['w', 'r', 'l', 'o', 'd']
        points = self.game_two.update_points()
        self.assertEqual(7, points, f'Points for \'world\' should be 7 and not {points}')

    def test_update_points_python_right(self):
        self.game_two.word = 'python'
        self.game_two.word_display = list('python')
        self.game_two.incorrect_guesses = ['k']
        self.game_two.correct_guesses = ['h', 'o', 't', 'p', 'n', 'y']
        points = self.game_two.update_points()
        self.assertEqual(13, points, f'Points for \'python\' should be 13 and not {points}')

    def test_update_points_python_guessing(self):
        self.game_two.word = 'python'
        self.game_two.word_display = list('pyt__n')
        self.game_two.incorrect_guesses = ['k']
        self.game_two.correct_guesses = ['t', 'p', 'n', 'y']
        points = self.game_two.update_points()
        self.assertEqual(0, points, f'Points for an unfinished \'pyt__n\' should be 0 and not {points}')

    def test_update_points_javascript_wrong_1(self):
        self.game_two.word = 'javascript'
        self.game_two.word_display = list('javascrip_')
        self.game_two.incorrect_guesses = ['n', 'o', 'l', 'q', 'b', 'y']
        self.game_two.correct_guesses = ['i', 'a', 'v', 'j', 's', 'c', 'r', 'p']
        points = self.game_two.update_points()
        self.assertEqual(0, points, f'Points for \'javascrip_\' should be 0 and not {points}')

    def test_update_points_javascript_wrong_7(self):
        self.game_two.word = 'javascript'
        self.game_two.word_display = list('j_v_s_____')
        self.game_two.incorrect_guesses = ['n', 'o', 'l', 'q', 'b', 'y']
        self.game_two.correct_guesses = ['v', 'j', 's']
        points = self.game_two.update_points()
        self.assertEqual(-5, points, f'Points for \'j_v_s_____\' should be -5 and not {points}')

    def test_update_list_of_words_and_reset_game(self):
        self.game_one.set_word()
        self.game_one.word = 'hello'
        self.game_one.word_display = list('hello')
        self.game_one.reset_game()
        self.assertIn('hello', self.game_one.words_played, 'Word not present in words played set')
        self.assertIn('hello', self.game_one.words_guessed, 'Word not present in the correctly guessed set')
        self.assertEqual(2, self.game_one.game_number, 'The game class number is incorrect')

        self.game_one.set_word()
        self.game_one.word = 'javascript'
        self.game_one.word_display = list('j_v_s_____')
        self.game_one.incorrect_guesses = ['n', 'o', 'l', 'q', 'b', 'y']
        self.game_one.correct_guesses = ['v', 'j', 's']
        self.game_one.reset_game()
        self.assertIn('javascript', self.game_one.words_played, 'Word not present in words played set')
        self.assertNotIn('javascript', self.game_one.words_guessed, 'Word not present in the correctly guessed set')
        self.assertIn('hello', self.game_one.words_played, 'Word not present in words played set')
        self.assertIn('hello', self.game_one.words_guessed, 'Word not present in the correctly guessed set')
        self.assertEqual(3, self.game_one.game_number, 'The game class number is incorrect')


if __name__ == '__main__':
    main()
