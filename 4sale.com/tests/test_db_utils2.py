import pytest
import sys 
import numpy as np
sys.path.append('..')
from db_utils import *

def test_db_utils():
	my_db = db("localhost","forsale","root","root")
	conn = my_db.get_connection()
	result = my_db.query_string_from_dict("properties",{'pid':1})
	assert result == "select * from properties where pid=1";