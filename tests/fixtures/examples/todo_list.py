todos = None
action = None


todos = []
while True:
  print('--- Todo List ---')
  # add enumerate loop to show todos here
  action = input('(a)dd / (r)emove / (q)uit: ')
  if action == 'a':
    todos.append(input('New todo: '))
  elif action == 'r':
    # add remove logic here
  elif action == 'q':
    break
