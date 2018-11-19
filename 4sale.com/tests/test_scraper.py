import pytest
import sys 
import numpy as np
sys.path.append('..')
from scraper import *

def create():
	try:
		scrap = Scraper()
		return True
	except:
		return False

def test_create():
	assert create()==True

