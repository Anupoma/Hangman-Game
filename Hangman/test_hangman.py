import pytest
import threading
import time
from hangman import HangmanGame

def test_basic():
    game = HangmanGame(level="basic")
    word = game.generate_word()
    assert isinstance(word, str)
    assert len(word) > 0

def test_intermediate():
    game = HangmanGame(level="intermediate")
    phrase = game.generate_word()
    assert isinstance(phrase, str)
    assert " " in phrase
    
def test_dictionary_word(monkeypatch):
    import builtins
    real_open = builtins.open

    def fake_open(*args, **kwargs):
        raise FileNotFoundError

    builtins.open = fake_open
    game = HangmanGame()
    words = game.load_words()
    assert "python" in words
    builtins.open = real_open  # restore
    
def test_display_word():
    game = HangmanGame()
    game.word = "python"
    game.guessed_letters = []
    assert game.get_display_word() == "______"
    
def test_phrase_keeps_spaces():
    game = HangmanGame()
    game.word = "hello world"
    assert game.get_display_word() == "_____ _____"

def test_timer_with_mocks(monkeypatch):
    """Test timer using mocks for better reliability."""
    sleep_calls = []
    life_deductions = []
    
    # Mock time.sleep to track calls without actually sleeping
    def mock_sleep(seconds):
        sleep_calls.append(seconds)
    
    # Mock life deduction to track without affecting game state
    original_deduct_life = HangmanGame.guess_letter
    
    def mock_deduct_life(self, letter):
        if letter == "_TIMER_EXPIRED_":
            life_deductions.append(1)
        else:
            return original_deduct_life(self, letter)
    
    monkeypatch.setattr(time, 'sleep', mock_sleep)
    monkeypatch.setattr(HangmanGame, 'guess_letter', mock_deduct_life)
    
    game = HangmanGame()
    game.start_timer()
    
    # Simulate timer behavior
    game.time_up = True
    
    # Verify timer attempted to sleep
    assert len(sleep_calls) > 0
    
def test_timer_deducts_life(monkeypatch):
    game = HangmanGame(lives=3)

    # Monkeypatch time.sleep to speed up test (no actual delay)
    monkeypatch.setattr(time, "sleep", lambda x: None)

    # Start timer
    game.start_timer()

    # Wait a little so the thread finishes execution
    game.timer_thread.join()

    # Since time_up was never set to True, life should be deducted
    assert game.lives == 2
    
def test_reveals_all_positions():
    game = HangmanGame()
    game.word = "banana"
    game.guess_letter("a")
    assert game.get_display_word() == "_a_a_a"
    
def test_guess_letter_correct():
    game = HangmanGame()
    game.word = "python"
    result = game.guess_letter("p")
    assert result is True
    assert "p" in game.guessed_letters
    assert game.get_display_word().startswith("p")

def test_guess_letter_incorrect():
    game = HangmanGame(lives=3)
    game.word = "python"
    result = game.guess_letter("x")
    assert result is False
    assert game.lives == 2

def test_repeated_guess():
    game = HangmanGame(lives=3)
    game.word = "apple"
    game.guess_letter("z")  # wrong
    lives_before = game.lives
    result = game.guess_letter("z")  # repeat
    assert result is None
    assert game.lives == lives_before

def test_win():
    game = HangmanGame()
    game.word = "hi"
    game.guessed_letters = ["h", "i"]
    assert game.is_won() is True

def test_lose():
    game = HangmanGame(lives=0)
    assert game.is_lost() is True
