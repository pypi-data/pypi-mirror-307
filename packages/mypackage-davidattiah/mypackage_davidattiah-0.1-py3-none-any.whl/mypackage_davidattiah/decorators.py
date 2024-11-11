import time
from functools import wraps
from contextlib import ContextDecorator

# Code Number 1
# Define the decorator
def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record start time
        result = func(*args, **kwargs)  # Call the function
        end_time = time.time()  # Record end time
        elapsed_time = end_time - start_time  # Calculate time difference
        print(f"Time taken by {func.__name__}: {elapsed_time:.6f} seconds")
        return result
    return wrapper

# Code Number 2
# Define the decorator with an argument
def timeit(min_seconds=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()  # Record start time
            result = func(*args, **kwargs)  # Call the function
            end_time = time.time()  # Record end time
            elapsed_time = end_time - start_time  # Calculate time difference
            
            if elapsed_time > min_seconds:
                print(f"Time taken by {func.__name__}: {elapsed_time:.6f} seconds")
            return result
        return wrapper
    return decorator

# Code Number 3
# Define the decorator with optional arguments
def timeit(func=None, *, min_seconds=0):
    if func and callable(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            if elapsed_time > min_seconds:
                print(f"Time taken by {func.__name__}: {elapsed_time:.6f} seconds")
            return result
        return wrapper

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            if elapsed_time > min_seconds:
                print(f"Time taken by {func.__name__}: {elapsed_time:.6f} seconds")
            return result
        return wrapper

    return decorator

# Code Number 4
# Repeating the same timeit definition as before...

# Code Number 5
# Define the decorator with debug option
def timeit(func=None, *, min_seconds=0):
    if func and callable(func):
        @wraps(func)
        def wrapper(*args, debug=False, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if debug and elapsed_time > min_seconds:
                print(f"Time taken by {func.__name__}: {elapsed_time:.6f} seconds")
            return result
        return wrapper

    def decorator(func):
        @wraps(func)
        def wrapper(*args, debug=False, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time

            if debug and elapsed_time > min_seconds:
                print(f"Time taken by {func.__name__}: {elapsed_time:.6f} seconds")
            return result
        return wrapper

    return decorator

# Code Number 6
# Create the timeit class as both context manager and decorator
class timeit(ContextDecorator):
    def __init__(self, min_seconds=0):
        self.min_seconds = min_seconds

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *exc):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        if self.elapsed_time > self.min_seconds:
            print(f"Time taken: {self.elapsed_time:.6f} seconds")

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapped_func

# Example functions
@timeit(min_seconds=1)
def slow_function():
    """This is a slow function that simulates a long task."""
    time.sleep(1.5)
    print("Slow function executed.")

if __name__ == "__main__":
    # Example usage as a context manager
    with timeit(min_seconds=1):
        time.sleep(1.5)  # Simulate a slow operation

    # Call the decorated function
    slow_function()  # Call the function and check the docstring
    print(slow_function.__doc__)

    # Call the function with debug=True
    slow_function(debug=True)  # Time output if debug is True
