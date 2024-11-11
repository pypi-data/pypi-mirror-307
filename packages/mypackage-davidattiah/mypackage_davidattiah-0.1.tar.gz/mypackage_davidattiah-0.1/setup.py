from setuptools import setup, find_packages

setup(
    name='mypackage_davidattiah',  # Updated package name
    version='0.1',  # Keep the version the same, or update it if needed
    packages=find_packages(),
    description='A package sample with generators, iterators, decorators, and descriptors', 
    author='David Attiah', 
    author_email='davidkumah@gmail.com', 
    url='https://github.com/david-attiah/mypackage_davidattiah',  # Updated GitHub link
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
