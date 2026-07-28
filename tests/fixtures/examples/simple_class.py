my_dog = None
name = None
breed = None


class Dog:
  def __init__(self, name, breed):
    self.name = name
    self.breed = breed
  def bark(self):
    print(f'{self.name} says Woof!')
my_dog = Dog("Rex", "Labrador")
