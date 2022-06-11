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

#1



def make_static_templates(projects):
	try:
		os.mkdir("templates")
	except:
		shutil.rmtree('templates')
		os.mkdir("templates")
	try:
		os.mkdir("static")
		os.mkdir("static/showcase")
	except:
		shutil.rmtree('static')
		os.mkdir("static")
		os.mkdir("static/showcase")
	
	for obj in projects:
		os.mkdir(f"templates/{obj.root[9:]}")
		

def save_objects(klass, filename):
	for a in get_folders():
		klass(root=a)
	with open(filename, 'wb') as file:
		pickle.dump(DProject.instances, file)



def load_objects(pickle_file):
	with open(pickle_file, 'rb') as file:
		files = pickle.load(file)
	return files





#2
def get_base_add(obj):
	soup = BeautifulSoup(open(f"{obj.root}/main/templates/base.html"), features="html.parser")
	base_links = [a for a in soup.head.find_all("link")]
	for a in base_links:
		try:
			a['href'] = a['href'].replace("css/", f"{obj.root[9:]}/css/")
		except:
			pass	
	
	base_scripts = [a for a in soup.find_all("script")]
	for a in base_scripts:
		a['src'] = a['src'].replace("js/", f"{obj.root[9:]}/js/")
	return base_links, base_scripts
		
#3
def move_js_css(obj):
	css_in_folder = get_dir_files(f"{obj.root}/static/css", ".css")
	js_in_folder = get_dir_files(f"{obj.root}/static/js", ".js")
	old_css = f"{obj.root}/static/css"		
	new_css = f"static/{obj.root[9:]}/css"
	old_js = f"{obj.root}/static/js"		
	new_js = f"static/{obj.root[9:]}/js"
	shutil.copytree(old_css, new_css)
	shutil.copytree(old_js, new_js)

#4
def write_new_partials(obj):
	base_links, base_scripts = get_base_add(obj)
	partials = obj.partials
	for file in partials:
		soup = BeautifulSoup(open(f"{obj.partial_templates}{file}"), features="html.parser")
		with open(f"templates/{obj.root[9:]}/{file}", "w", encoding="utf-8") as new_file:
			new_file.write( str(base_links).replace("[", "").replace("]", "").replace("," , " ").replace("> ", ">\n"))
			new_file.write("\n")
			new_file.write(str(soup).replace("img/", "showcase/"))
			new_file.write("\n")
			new_file.write( str(base_scripts).replace("[", "").replace("]", "").replace("," , " ").replace("> ", ">\n"))


def write_new_css(obj):
	all_css = get_dir_files(f"static/{obj.root[9:]}/css", ending="css")
	exclude_aos = [file for file in all_css if "aos" not in file ]
	css_file = min(exclude_aos, key=len)
	print(obj.root[9:], css_file)
	with open(f"static/{obj.root[9:]}/css/{css_file}", "r", encoding="utf-8") as old:
		old_file = old.read()
		
	old_file = old_file.replace("../img/", "../showcase/")
	old_file = old_file.replace("/static/img/", "/static/showcase/")	
	
	print(old_file)
	os.remove(f"static/{obj.root[9:]}/css/{css_file}")
	with open(f"static/{obj.root[9:]}/css/{css_file}", "w", encoding="utf-8") as new_file:
		new_file.write(old_file)

def move_img_to_showcase():
	root = "C:/Users/Abrahan/Desktop/django-trimmer/trim/__BOOTSTRAP"
	#projects = load_objects("projects")
	img_files = []
	for root, subdirs, files in os.walk(root):    
		for file in files:
			if file.endswith(("jpg", "jpeg", "svg", "gif", "png")):
				if file not in img_files:
					img_files.append(file)
					shutil.copy(f"{root}/{file}", f"static/showcase/{file}")
				else:
					pass	


if __name__ == "__main__":
	#save_objects(klass=DProject, filename="projects")
	projects = load_objects("projects")
	service_templates = []
	for project in projects:
		path = f"C:/Users/Abrahan/Desktop/templates/{project.root[9:]}" 
		files = get_dir_files(root=path, ending="html")
		for file in files:
			with open(f"{path}/{file}", "r", encoding="utf-8") as old:
				old_file = old.read()
				load_static = "{% load static %}\n"
			
			os.remove(f"{path}/{file}")
			with open(f"{path}/{file}", "w", encoding="utf-8") as new_file:
				new_file.write(str(load_static))
				new_file.write(str(old_file))
