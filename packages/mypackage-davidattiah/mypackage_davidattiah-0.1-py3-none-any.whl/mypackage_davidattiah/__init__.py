# mypackage/__init__.py
import sys

# Import each module (assuming they're named generators.py, iterators.py, etc.)
from . import generators
from . import iterators
from . import decorators
from . import descriptors

def main():
    print("Launching mypackage")

    # Execute code from each module if they have a main function or relevant functions
    print("\nRunning generators module:")
    generators.main()  # Assuming `main` exists in generators.py

    print("\nRunning iterators module:")
    iterators.main()   # Assuming `main` exists in iterators.py

    print("\nRunning decorators module:")
    decorators.main()  # Assuming `main` exists in decorators.py

    print("\nRunning descriptors module:")
    descriptors.main() # Assuming `main` exists in descriptors.py

if __name__ == "__main__":
    main()
