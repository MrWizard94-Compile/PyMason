text = None
words = None
counts = None
word = None


text = input('Enter text: ')
words = text.lower().split(' ')
counts = {}
for word in words:
  # use dict get/set to count each word
print(f'Word count: {len(words)} — finish counting with the dict!')
