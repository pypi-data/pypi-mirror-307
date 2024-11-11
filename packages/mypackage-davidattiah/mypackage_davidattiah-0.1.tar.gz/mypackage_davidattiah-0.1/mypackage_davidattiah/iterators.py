# Task 1: Iterator for numbers from 10 to a given limit
class NumberIterator:
    def __init__(self, limit):
        self.current = 10
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.limit:
            result = self.current
            self.current += 1
            return result
        else:
            raise StopIteration

# Example usage:
if __name__ == "__main__":
    for num in NumberIterator(20):
        print(num)

# Task 2(A): Infinite iterator for numbers divisible by 7 and 9
from itertools import count

def divisible_by_7_and_9():
    for num in count(0):  # Infinite iterator starting from 0
        if num % 7 == 0 and num % 9 == 0:
            yield num

# Example usage:
if __name__ == "__main__":
    div_gen = divisible_by_7_and_9()
    for _ in range(5):
        print(next(div_gen))

# Task 2(B): Repeat a string 15 times
from itertools import repeat

def repeat_string(string, times=15):
    return repeat(string, times)  # Using itertools.repeat to create the iterator

# Example usage:
if __name__ == "__main__":
    for s in repeat_string("Hello"):
        print(s)

# Task 2(C): Repeat a value 38 times
def repeat_value(value, times=38):
    return (value for _ in range(times))  # Generator expression

# Example usage:
if __name__ == "__main__":
    for val in repeat_value(42):
        print(val)

import itertools

# Task 3(A): Iterator for all permutations of a list
def permutations_list(lst):
    return itertools.permutations(lst)

# Example usage:
if __name__ == "__main__":
    for perm in permutations_list([1, 2, 3]):
        print(perm)

# Task 3(B): Iterator for all combinations of a list without replacement
def combinations_list(lst):
    result = []
    for r in range(1, len(lst) + 1):
        result.extend(itertools.combinations(sorted(lst), r))
    return result

# Example usage:
if __name__ == "__main__":
    for comb in combinations_list([3, 1, 2]):
        print(comb)

# Task 4: Iterator to transform phrases
class PhraseTransformer:
    def __init__(self, phrases):
        self.phrases = phrases
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.phrases):
            raise StopIteration
        
        phrase = self.phrases[self.index]
        self.index += 1
        
        # Remove 'of' and convert plural nouns to singular (naive approach)
        transformed = phrase.replace(" of ", " ").replace("s ", " ")
        return transformed

# Example usage:
if __name__ == "__main__":
    phrases = ["list of books", "collection of cars", "group of dogs"]
    for transformed in PhraseTransformer(phrases):
        print(transformed)
