import pytest
import sys 
import numpy as np
sys.path.append('..')
from db_utils import *

def create():
	try:
		my_db = db("localhost","forsale","root","root")
		return True
	except:
		return False

def test_create():
	assert create()==True
