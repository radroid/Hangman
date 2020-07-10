from unittest import mock, TestCase, main
from ..hangman_pack import HangmanGame


class TestGamePlay(TestCase):

    def setUp(self):
        """ Creates GamePlay class for all the unittests. """
        self.game_one = HangmanGame()
        self.game_two = HangmanGame()

    def test_set_word(self):
        """ Checks if the word is set correctly. """
        self.game_one.set_word()
        self.assertIsNotNone(self.game_one.word, "Variable 'word' is empty")
        self.assertEqual(len(self.game_one.word_display), len(self.game_one.word), "Length of 'word_display' and "
                                                                                   "'word' do not match. ")
        self.assertIn('_', self.game_one.word_display, "'word_display' does not contain dashes: '_'")

    def test_word_display(self):
        pass

    def test_guess_letter(self):
        # TODO: write a tests to check if update guessed_letters, correct_guesses, incorrect_guesses, Hangman are
        #  updated correctly. Use mock.
        pass

    def test_get_valid_guess(self):
        # TODO: write a tests using mock to check for all different inputs.
        pass

    def test_update_word_display(self):
        self.game_one.set_word()
        letter = self.game_one.word[1]
        self.game_one.update_word_display(letter)
        self.assertEqual(self.game_one.word_display[1], letter,
                         "'word_display' is not updated correctly. The second letter should be displayed.")

    def test_update_hangman(self):
        self.game_one.incorrect_guesses = ['a']
        self.game_one.update_hangman()
        self.assertEqual(self.game_one.hangman.get('head'), 'O', "Hangman's head was not updated.")

        self.game_one.incorrect_guesses = ['a', 'b']
        self.game_one.update_hangman()
        self.assertEqual(self.game_one.hangman.get('body'), '|', "Hangman's body was not updated.")

        self.game_one.incorrect_guesses = ['a', 'b', 'c']
        self.game_one.update_hangman()
        self.assertEqual(self.game_one.hangman.get('right_hand'), '/', "Hangman's right_hand was not updated.")

        self.game_one.incorrect_guesses = ['a', 'b', 'c', 'd']
        self.game_one.update_hangman()
        self.assertEqual(self.game_one.hangman.get('left_hand'), '\\', "Hangman's left_hand was not updated.")

    def test_get_status(self):
        self.game_one.set_word()
        self.game_one.word = 'hello'
        self.assertEqual(self.game_one.get_status(), 'guessing', "Initial state of the game is incorrect")
        self.game_one.word_display = ['h', 'e', 'l', 'l', 'o']
        self.game_one.set_status()
        self.assertEqual(self.game_one.get_status(), 'won', "State of a game won is incorrect")

        self.game_two.set_word()
        self.game_two.word = 'world'
        self.assertEqual(self.game_two.get_status(), 'guessing', "Initial state of the game is incorrect")
        self.game_two.word_display = ['w', 'o', 'r', 'l', '_']
        self.game_two.incorrect_guesses = ['i', 'p', 't', 'q', 's', 'n']
        self.game_two.set_status()
        self.assertEqual(self.game_two.get_status(), 'lost', "State of a game lost is incorrect")

    def test_update_points(self):
        # TODO: Define a method to update total_points
        pass

    def test_update_list_of_words(self):
        # TODO: Define a method to add words to words_played and words_guessed
        pass

    def test_initialise_all(self):
        # TODO: write a tests to check all variables are initialised
        pass

    def test_initialise_guesses(self):
        # TODO: write a tests to check certain variables are initialised
        pass


if __name__ == '__main__':
    main()
