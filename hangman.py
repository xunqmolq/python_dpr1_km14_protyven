# Problem Set 2, hangman.py
# Name:  Oleh Protyven
# Collaborators: with music
# Time spent: 3-4 hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
import os
from collections import Counter
WORDLIST_FILENAME = "words.txt"

"""
  Returns placement this file and change directory on desired direction
"""
x = os.path.abspath(__file__).replace("\\hangman.py", "")
os.chdir(x)

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_letters = []
    for i in secret_word:
      secret_letters.append(i)
    if set(secret_letters) & set(letters_guessed) == set(secret_letters):
      return True
    else:
      return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

    guessed = []
    for i in secret_word:
      if i in letters_guessed:
        guessed.append(i)
      else:
        guessed.append("_ ")
    guessed_word = "".join(guessed)
    return guessed_word  
    
def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    aviable_letters = string.ascii_lowercase
    for i in letters_guessed:
      if i in aviable_letters:
        aviable_letters = aviable_letters.replace(i,"")
    return aviable_letters

def check(letter):
  '''
  This function check entered value of letter. It returns False if entered value is not one letter.
  letter = string, element entered by user.
  '''
  try:
    if len(letter) != 1:
      raise Exception
    elif letter.isalpha() is False:
      raise Exception
    else:
      return True
  except Exception:
    print ("Please enter one letter!")
    return False    
    
def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    lifes = 6
    letters_guessed = []
    letter = str()
    print ("============================================\nWelcome to the game Hangman!\nI am thinking of a word that is", len(secret_word), "letters long.\n=============================================")
    def print_():
      '''
      This function prints template.
      '''
      print ("You have",lifes, "guesses left.")
      print (get_guessed_word(secret_word, letters_guessed))
      print ("Aviable letters: ",get_available_letters(letters_guessed), "\n---------------------------------")
    print_()
    def inp_letter():
      '''
      This function processes the entered value. 
      '''
      counter = 3
      while True:
        nonlocal lifes
        if counter == 0:
          lifes -= 1
          print ("Sorry, you ran out of warnings. You have",lifes, "guesses left.")
          counter = 3
        letter = input("Please guess a letter: ")
        letter = str.lower(letter)
        if check(letter):
          break
        else:
          print ("You have", counter,"warnings left.")
          counter -= 1
      return letter  


    while lifes > 0:
      vowel = ["a","e","i","o"]
      if is_word_guessed(secret_word, letters_guessed) is False:
        letter = inp_letter()
        if letter not in get_available_letters(letters_guessed):
          print ("You have already entered this letter!")
          lifes -= 1
        elif letter in secret_word:
          letters_guessed.append(letter)
        else:
          print ("Oops! That letter is not in my word.")
          letters_guessed.append(letter)
          if letter in vowel:
            if lifes > 1:
              lifes -= 2
            else:
              lifes -= 1 # Lifes can't be negative value
          else:
            lifes -=1
        print_()
      else:
        print ("Congratulations, you won!")
        score = lifes*len(set(secret_word))
        print ("Your score:",score)
        break
    if is_word_guessed(secret_word, letters_guessed) is False:
      print ("Sorry, you ran out of guesses. The word was", secret_word)
      

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_splited = str(my_word).split()
    my_w = list(''.join(my_word_splited))
    other_w = list(other_word)
    if len(my_w) != len(other_w):
      return False
    bool = True
    counter = 0
    val = Counter(my_w)
    val_o = Counter(other_w)
    for i in range (len(my_w)):
      if my_w[i] == "_":
        counter += 1
      elif my_w[i] == other_w[i]:
        if val[my_w[i]] == val_o[other_w[i]]: 
          counter += 1
        else:
          bool == False
      else:
        bool = False
    if bool == False or counter != len(my_w):
      return False
    else:
      return True

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    match = str()
    for i in wordlist:
      if match_with_gaps(my_word, i):
        match = match+" "+i
    if match == ():
      print ("No matches found")
    else:
      print(match)

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    lifes = 6
    letters_guessed = []
    letter = str()
    print ("============================================\nWelcome to the game Hangman!\nI am thinking of a word that is", len(secret_word), "letters long.\n=============================================")
    def print_():
      '''
      This function prints template.
      '''
      print ("You have",lifes, "guesses left.")

      print (get_guessed_word(secret_word, letters_guessed))
      print ("Aviable letters: ",get_available_letters(letters_guessed), "\n -----------------------------")
    print_()
    def inp_letter():
      '''
      This function processes the entered value. 
      '''
      counter = 3
      while True:
        nonlocal lifes
        if counter == 0:
          lifes -= 1
          print ("Sorry, you ran out of warnings. You have",lifes, "guesses left.")
          counter = 3
        letter = input("Please guess a letter: ")
        if letter == "*":
          break
        letter = str.lower(letter)
        if check(letter):
          break
        else:
          print ("You have", counter,"warnings left.")
          counter -= 1
      return letter  


    while lifes > 0:
      vowel = ["a","e","i","o"]
      hints = 0
      if is_word_guessed(secret_word, letters_guessed) is False:
        letter = inp_letter()
        if letter == "*":
          if hints == 0:
            print("Possible word matches are:", end= " ")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            """
              Uncomment code below if you want to make 1 hint
            """
            #hints +=1
          #else:
           # print("You haven't hints anymore")
        elif letter not in get_available_letters(letters_guessed):
          print ("You have already entered this letter!")
        elif letter in secret_word:
          letters_guessed.append(letter)
        else:
          print ("Oops! That letter is not in my word.")
          letters_guessed.append(letter)
          if letter in vowel:
            if lifes > 1:
              lifes -= 2
            else:
              lifes -= 1 # Lifes can't be negative value
          else:
            lifes -=1
        print_()
      else:
        print ("Congratulations, you won!")
        score = lifes*len(set(secret_word))
        print ("Your score:",score)
        break
    if is_word_guessed(secret_word, letters_guessed) is False:
      print ("Sorry, you ran out of guesses. The word was", secret_word)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
