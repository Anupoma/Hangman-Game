import random
import time
import threading

hangman_art= {0: (" ",
                  " ",
                  " "), 
              1: (" o ",
                  "   ",
                  "   "), 
              2: (" o ",
                  "| ",
                  "   "), 
              3: (" o ",
                  "/|",
                  "    "), 
              4: (" o  ",
                  "/|\\",
                  "    "), 
              5: (" o  ",
                  "/|\\",
                  "/   "), 
              6: (" o  ",
                  "/|\\",
                  "/ \\ ")}

class HangmanGame:
    def __init__(self, level="basic", lives=6):   
        self.level = level  
        self.lives = lives
        self.max_lives = lives
        self.word_list = self.load_words()
        self.word = ""
        self.guessed_letters = []
        self.timer_thread = None
        self.time_up = False
        self.timer = 15

    def load_words(self):
        try:
            with open("words.txt", "r") as f:
                words = [line.strip() for line in f if line.strip()]
            return words
        except FileNotFoundError: 
            return ["python", "hangman", "testing", "programming", "unit", "test"]

    def generate_word(self):
        if self.level == "basic":
            self.word = random.choice(self.word_list)
        elif self.level == "intermediate":
            # Ensure we have enough words for a phrase
            if len(self.word_list) >= 2:
                self.word = random.choice(self.word_list) + " " + random.choice(self.word_list)
            else:
                self.word = random.choice(self.word_list)
        return self.word

# This function shows the word with underscores (_) for letters
    def get_display_word(self): 
        display = ""
        for ch in self.word: #Check character in the words
            if ch == " ":
                display += " "
            elif ch.lower() in self.guessed_letters: #If user guessed ch; display
                display += ch
            else:
                display += "_" #If can't guess; show '_'
        return display

 #Timer
    def start_timer(self):
        self.time_up = False
        self.timer = 15

        def countdown():
            for i in range(15, 0, -1):
                if self.time_up:
                    return
                self.timer = i
                time.sleep(1)
            
            if not self.time_up:  # if user hasn't guessed yet
                self.lives -= 1
                print("\nTime's up! You lost a life.")
                self.display_hangman_art()
                
        self.timer_thread = threading.Thread(target=countdown, daemon=True)
        self.timer_thread.start()
        
#This function checks guessed letters
    def guess_letter(self, letter):
        letter = letter.lower()     #Convert all letters to lowercase
        
        if letter in self.guessed_letters:
            return None  # already guessed then no life take away
        self.guessed_letters.append(letter) #Add letters to the guessed letters list
       
        if letter in self.word.lower(): #If letter is in the word
            return True 
        else:
            self.lives -= 1 #If letter is not present in the word; kill one 
            return False
        
#if the player has guessed the whole word.
    def is_won(self):
        for ch in self.word.lower():
            if ch.isalpha() and ch not in self.guessed_letters:
                return False    #if there are still missing letters
        return True  #if all letters have been guessed
#if the player has run out of lives.
    def is_lost(self):
        return self.lives <= 0
    
#Hangman art
    def display_hangman_art(self):
        
        lives_lost = self.max_lives - self.lives
        if lives_lost > 6:
            lives_lost = 6
        art = hangman_art[lives_lost]
        for line in art:
            print(line)        
# Time and Quit Option
    def play(self):
        self.generate_word()
        print("************Welcome to Hangman!**************")
        print(f"Level: {self.level.capitalize()}")
        print(f"You have {self.lives} lives. Good luck!\n")

        while not self.is_won() and not self.is_lost():
            print("\nWord:", self.get_display_word())
            print(f"Lives: {self.lives}")
            self.display_hangman_art()
            # Start the timer for this turn
            self.start_timer()
            try:
                guess = input(f"Time left: {self.timer}s - Enter a letter (or 'quit' to exit): ")
            except EOFError:
                print("\n########Thanks for playing!###########")
                return
                
            self.time_up = True  # stop timer once input is received
            if guess.lower() == "quit":
                print("########Thanks for playing!#########")
                return
            if len(guess) != 1 or not guess.isalpha():
                print("!!Please enter a single letter.")
                continue
            result = self.guess_letter(guess)
            if result is True:
                print(f"Good guess: {guess}")
            elif result is False:
                print(f"Wrong guess: {guess}")
                self.display_hangman_art()
            else:
                print(f"Already guessed: {guess}")
        if self.is_won():
            print(f"*******Congratulations! You guessed the word: {self.word}*******")
        else:
            print(f"Game Over! The word was: {self.word}")
            self.display_hangman_art()
            
if __name__ == "__main__":
    choice = input("Choose level (basic/intermediate): ").strip().lower()
    if choice not in ["basic", "intermediate"]:
        choice = "basic"
    game = HangmanGame(level=choice, lives=6)
    game.play()