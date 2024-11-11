def add(a, b):
  """
  Adds two numbers together.

  Example:
  >>> add(2, 3)
  5
  >>> add(0, 0)
  0
  >>> add(-1, 1)
  0
  """
  return a + b


class Calculator:
  """
  A simple calculator class.

  Example:
  >>> calc = Calculator()
  >>> calc.add(2, 3)
  5
  >>> calc.subtract(5, 3)
  2
  """

  def add(self, a, b):
    return a + b

  def subtract(self, a, b):
    return a - b

if __name__ == "__main__":
  # import doctest
  # doctest.testmod()

  import sys 
  sys.path.append('.')
  from c4dynamics.datasets._manager import sha256 
  print(sha256(r'C:\Users\odely\Downloads\drifting_car.mp4'))







