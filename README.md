# Hangman-Game
A classic word-guessing game implemented in Python using *Test Driven Development (TDD)* and *automated unit testing with Pytest*.  
This project focuses on creating a reliable, interactive, and user-friendly version of Hangman with modular code and comprehensive test coverage. It includes a 15-second guess timer, life tracking, and visual representation of the hangman state.

---

## 📁 Repository Structure

```plaintext
Hangman-Game/
├── hangman.py          # Main game logic
├── test_hangman.py     # Unit tests using Pytest
├── words.txt           # Word dictionary for the game
├── docs/               # Documentation or report files
└── README.md           # Project documentation
```
🎯 Features

- Random word or phrase selection from a dictionary  
- Displays partially revealed word with underscores for unguessed letters  
- 15-second timer for each guess (life deducted if time runs out)  
- Reveals all positions of correctly guessed letters  
- Deducts lives for wrong guesses  
- Win/loss evaluation system  
- Option to quit anytime  
- Clean and modular Python code for easy understanding  
- Fully tested with *Pytest*

🧪 Test-Driven Development (TDD)

The Hangman game was developed using *TDD (Test-Driven Development)*, following these steps:

1. *Write Tests First* – Create unit tests for each function before implementing the code.  
2. *Implement Code* – Write code to make the test cases pass.  
3. *Refactor* – Improve code readability and remove duplication while ensuring tests still pass.  

Unit tests cover key functionalities including:

- Word generation (basic and intermediate levels)  
- Hidden letter handling  
- Letter reveal mechanism  
- Life deduction for wrong guesses  
- Timer-based guess penalty  
- Game outcome evaluation (win/loss)
