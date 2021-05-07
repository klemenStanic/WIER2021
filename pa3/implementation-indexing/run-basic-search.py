import utils
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please enter query string.')
        sys.exit()

    q = sys.argv[1]
