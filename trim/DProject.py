import os
from bs4 import BeautifulSoup
from collections import OrderedDict
from utils import *
import logging

class DProject(object):
	root = None
	
	def __init__(self, root):
		self.root = root
		self.main = f"{self.root}/main/"
		self.static = f"{self.root}/static/"
		self.main_templates = f"{self.root}/main/templates/main/"
		self.partial_templates = f"{self.root}/main/templates/partials/"
		self.urls = f"{self.root}/main/templates/main/urls.py"
		self.views = f"{self.root}/main/templates/main/views.py"


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


if __name__ == "__main__":
	project = DProject(root="myproject")
	project.send_partials()
	# for a in dir(project):
	# 	if str(a).startswith("__") == False:
	# 		print(f"---------------------{a}---------------------\n", eval(f"project.{a}"), "\n\n")