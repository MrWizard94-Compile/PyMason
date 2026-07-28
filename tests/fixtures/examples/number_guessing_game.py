import random

secret = None
guess = None


import random
secret = random.randint(1, 100)
guess = 0
while guess != secret:
  guess = int(input('Guess (1-100): '))
  if guess < secret:
    print('Too low!')
  elif guess > secret:
    print('Too high!')
  else:
    print('Correct! You guessed it!')
