def find(predicate, iterable):
  for element in iterable:
      if predicate(element):
          return element
  return None

def some(predicate, iterable):
    for element in iterable:
        if predicate(element):
            return True
    return False

def every(predicate, iterable):
    for element in iterable:
        if not predicate(element):
            return False
    return True

def findIndex(predicate, iterable):
  for index, element in enumerate(iterable):
      if predicate(element):
          return index
  return None
