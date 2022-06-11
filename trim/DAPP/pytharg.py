from utils import *
from DProject import *
from BTemplate import *
import pickle
from bs4 import BeautifulSoup
import shutil 
from BTemplate import BTemplate
from collections import OrderedDict
from pathlib import Path

import os

def load_objects(pickle_file):
	with open(pickle_file, 'rb') as file:
		files = pickle.load(file)
	return files


def create_project(project):
	try:
		shutil.rmtree(project)
		os.system(f"django-admin startproject {project}")
	except:
		os.system(f"django-admin startproject {project}")



def create_templates_static(projects=None, folder=None):

	try:
		os.mkdir(folder)	
	except:
		shutil.rmtree(folder)
		os.mkdir(folder)
	
	for project in projects:
		project.name = project.root[9:]
		if folder == "templates":
			os.mkdir(f"templates/{project.name}")
			os.mkdir(f"templates/{project.name}/partials")
			os.mkdir(f"templates/{project.name}/main")
			os.mkdir(f"templates/{project.name}/original")
		
		elif folder == "static":
			os.mkdir(f"static/{project.name}")
			os.mkdir(f"static/{project.name}/img")
			os.mkdir(f"static/{project.name}/css")
			os.mkdir(f"static/{project.name}/js")

		else:
			print("projects or folder passed == None")

		


if __name__ == "__main__":
	projects = load_objects("dprojects")
	
	for project in projects[1:2]:
		print(project.root)
		p = DProject(project="pytharg", root=f"{project.root[9:]}")
		t = BTemplate(template=f"{p.root.title()}", project=f"{p.root}")