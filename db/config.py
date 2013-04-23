#config.py
import os
def relative_project_path(*x):

    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

def parent_project_path(*x):
	return os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir)), *x)

def get_parent_path():
	return os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir))

DB_file = "dev.sqldb"
DB_path = relative_project_path(DB_file)