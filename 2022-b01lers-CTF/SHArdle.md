# SHArdle

```
score: 89 Points
solved: 73/89
difficulty: medium
tags: misc
```

## Problem

Five-letter words are for losers...
(btw, color terminal advised)
nc ctf.b01lers.com 9102

[code](SHArdle.py)

## Got the flag

### TL;DR
Prebuilt a map of SHA256: word from a [big word list](https://github.com/dwyl/english-words/blob/master/words_alpha.txt).
Use a list of 7 words (any word you can think of).
Then guess ~7 times, the result would gives us ~20+ characters & position of correct ones (green).
Find in the map which word have same SHA256 characters in the same positions, that would be the words.

This does not guarantee to solve in 1 run, but after several tries, we got the flag.

### Solution
Wrong assumption:

- input word has 5 chars only, like real Wordle: A hint from desc **five-letter words are for losers**, this is not limitted to five-letter words.
- input word may not be an English word but H4ck3r style-word?: try and it will fail with error invalid word.


```py
class Game:

   def __init__(self):
      self.rounds = 2
      self.secrets = [ generate(randint)   for i in range(self.rounds) ]
      self.start()

   def menu(self, round):
      print(f"1 - guess secret {round}")
      print( "2 - exit")
      print( "choose: ", end = "")

   def start(self):

      print( "I thought of some secrets, can you guess those?\n" )

      guesses = 15
      round = 0
      while guesses > 0:
         try:
            self.menu(round + 1)
            s = int( input("").strip() )
            if s == 2:  exit(0)
            elif s == 1:
               s = input("your guess: ").strip().encode().lower()
               if not valid(s):  print("INVALID GUESS")
               else:
                  print(f"score: {hashAndCompare(s, self.secrets[round])}")
                  if s == self.secrets[round]:
                     round += 1
                     print(f"BINGO!! {self.rounds - round} more to go")
                     if round == self.rounds:
                        print(f"Here is the flag: {FLAG}")
                        exit(0)
                  guesses -= 1
         except ValueError:
            print("invalid choice")
      print("No more guesses - goodbye!")
```

The logic here is clear, we have 15 guesses to guess 2 words. For each guess, server would compare SHA256 of the secret with SHA256 of input word, then returns green/yellow/gray color of each character, follow the rules of [Wordle](https://www.nytimes.com/games/wordle/index.html).

- green: guess correct
- yellow: the character is in result, but wrong position
- gray: the character not in result.

We try "hello" to see what server responses, each times it will returns different color because the word is randomized for each connection.

Parsing the result to get which are correct characters and positions. Then find in a pre-built dictionary of SHA256:word to find which words have hashes that match the secret, with enough correct characters, we can limit the number of possible words to very small number, at ~20 correct chars, the word is likely to be unique. Just make sure to get a big word list, which we can get [400k+ English words from here](https://github.com/dwyl/english-words/blob/master/words_alpha.txt).

```py
CODE TODO
```

Fun fact: our 2nd round word is `thermalnuclear`
