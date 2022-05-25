import os
import shutil
from bs4 import BeautifulSoup
from collections import OrderedDict
from utils import *
import logging
import subprocess
from BTemplate import BTemplate
import traceback
from bs4 import Comment
from time import sleep

class DProject(object):
	root = None
	
	def __init__(self, root):
		self.root = root
		self.main = f"{self.root}/main/"
		self.static = f"{self.root}/static/"
		self.main_templates = f"{self.root}/main/templates/main/"
		self.partial_templates = f"{self.root}/main/templates/partials/"
		self.urls = f"{self.root}/main/urls.py"
		self.views = f"{self.root}/main/views.py"


	@property
	def current_css_files(self):
		"""returns lsit of current .css files in static/img"""
		css_files = get_dir_files(root=f"{self.static}css", ending="css")
		return css_files
	

	@property	
	def current_js_files(self):
		"""returns lsit of current js files in static/img"""
		current_js_files = get_dir_files(root=f"{self.static}js", ending="js")
		return current_js_files


	@property	
	def current_img_files(self):
		"""returns lsit of current img files in static/img"""
		current_img_files = get_dir_files(root=f"{self.static}img", ending=("jpg", ".jpeg", ".png", ".gif", ".svg"))
		return current_img_files	

	
	@property	
	def sections(self):
		"""returns list of unduplicaded section ids in main pages"""
		sections = []
		for page in self.pages:
			soup = BeautifulSoup(open(f"{self.main_templates}{page}"), features="html.parser")
			page_sections = [ a['id'] for a in soup.find_all("section") ]
			sections += page_sections
		sections += ["header", "footer"]	
		sections = list(OrderedDict.fromkeys(sections))
		return sections			


	@property		
	def partials(self):
		"""returns list of htmls in  /partials"""
		partial_templates = get_dir_files(root=f"{self.partial_templates}", ending=(".html"))
		return partial_templates
	
	@property		
	def pages(self):
		"""returns list of htmls in /main"""
		pages = get_dir_files(root=f"{self.main_templates}", ending=(".html"))
		return pages



	def send_partials(self):
		"""send section chunks to indepentant html files"""
		sections = self.sections
		files = self.pages
		
		for section in sections:
			for file in files:
				try:
					soup = BeautifulSoup(open(f"{self.main_templates}{file}"), features="html.parser")
					section_div = soup.find(id=section)
					if section_div != None:
						with open(f"{self.partial_templates}{section}.html", "w") as section_html:
							section_html.write(load_static)
							section_html.write(f"<!-- ======= {section.capitalize()} Section ======= -->\n")
							section_html.write(str(section_div.prettify()))
							section_html.write(f"\n<!-- ======= End {section.capitalize()} Section ======= -->")

				except Exception as e:
					pass
					logging.error(traceback.format_exc())


	def prepare_project(self):
		#start project / app
		os.system(f"django-admin startproject {self.root}")
		os.chdir(self.root)
		os.system(f"python manage.py startapp main")
		#creat static
		os.mkdir("static")
		[os.mkdir(a) for a in ["static/css", "static/js", "static/img"]] 
		#crear templates
		os.chdir(os.path.join(os.getcwd(), "main"))
		os.mkdir("templates")
		[os.mkdir(a) for a in ["templates/main", "templates/partials", "templates/original"]] 



	def clean_main_templates(self):
		sections = self.sections
		files = self.pages	
		for file in files:
			soup = BeautifulSoup(open(f"{self.main_templates}{file}"), features="html.parser")
			for section in sections:
				try:
					section_div = soup.find(id=section)
					if section_div != None:
						clean_scripts = [a.extract() for a in soup.find_all("script") ]
						try:
							head = soup.find("head")
							head = head.extract()
						except:
							pass	
						section_unspaced = section.replace(" ", "-")
						include_text = f"\t{include_start} 'partials/{section_unspaced}.html' {include_end}\n"
						if (section == "header") or (section == "footer"):
							comment = Comment(f'==== extended from base.html ====-')
							section_div = section_div.replace_with(comment)
						else:
							section_div = section_div.replace_with(include_text)
						
				
				except Exception as e:
					logging.error(traceback.format_exc())
					pass

			with open(f"{self.main_templates}new_{file}", "w") as new_page_html:
				new_page_html.write(extends_base)
				new_page_html.write(load_static)
				new_page_html.write(block(file))
				soup = soup.prettify()
				new_page_html.write(str(soup))	
				new_page_html.write(endblock)



	def replace_img_srcs(self):
		images = self.current_img_files
		partials = self.partials
		for partial in partials:
			soup = BeautifulSoup(open(f"{self.partial_templates}{partial}"), features="html.parser")
			img_sources = [ img for img in soup.find_all("img") ]
			for image_file in images:
				for img in img_sources:
					if image_file in img["src"]:
						img['src'] = get_static_link(image_file, "img")
			print(img_sources)
			with open(f"{self.partial_templates}new_{partial}", "w") as new_partial:
				new_partial.write(str(soup).replace("&quot;", ""))
			os.remove(f"{self.partial_templates}{partial}")
			shutil.move(f"{self.partial_templates}new_{partial}", f"{self.partial_templates}{partial}")
			
	def move_unclean_to_original(self):
		pages = self.pages
		for page in pages:
			if page.startswith("new_") == False:
				shutil.move(f"{self.main_templates}{page}", f"{self.main}templates/original/{page}")
			
		for page in pages:
			if page.startswith("new_"):
				os.rename( f"{self.main_templates}{page}", f"{self.main_templates}{page.replace('new_', '')}")



if __name__ == "__main__":
	start_path = os.getcwd()
	new_project_name = input("que nombre le pones al proyecto\n")
	project = DProject(root=new_project_name)
	project.prepare_project()
	os.chdir(start_path)
	btemplate = BTemplate(template="Company", project=f"{project.root}")
	project.send_partials()
	project.clean_main_templates()
	btemplate.send_base_html()
	project.replace_img_srcs()
	project.move_unclean_to_original()
	print("_____________________________________________________________________")
	# for a in dir(project):
	# 	if str(a).startswith("__") == False:
	# 		sleep(3	)
	# 		print(f"---------------------{a}---------------------\n", eval(f"project.{a}"), "\n\n")
	# sleep(50)
	