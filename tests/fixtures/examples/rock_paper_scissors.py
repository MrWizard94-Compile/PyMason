choices = None
player = None
computer = None


import random
choices = ['rock', 'paper', 'scissors']
player = input('rock, paper, or scissors? ')
computer = random.choice(choices)
print(f'Computer chose: {computer}')
# add if/elif/else to determine winner
