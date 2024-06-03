import os

if os.name != 'posix':
    raise Exception('This package is only supported under WSL.')
