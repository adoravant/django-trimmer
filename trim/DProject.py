import os
from glob import glob
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
			page_sections = []
			renamed = []
			soup = BeautifulSoup(open(f"{self.main_templates}{page}"), features="html.parser")
			for section_div in soup.find_all("section"):
				try:
					page_sections.append(section_div['id'])
				except:
					section_div['id'] = section_div['class'][0] 
					page_sections.append(section_div['id'])
					renamed.append(section_div['id'])		
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
		start_path = os.getcwd()
		#check if template exists
		check_is_folder = get_folders(f"__BOOTSTRAP/{self.root.title()}")
		#create project
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
		os.chdir(start_path)


	def clean_main_templates(self):
		sections = self.sections
		print(f"\n-----sections found...........................\n{sections}")
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
				new_page_html.write("\n<head>\n\t<title>{{ page_title }}</title>\n</head>")
				soup = soup.prettify()
				new_page_html.write(str(soup).replace('<html lang="en">', '').replace("<!DOCTYPE html>", "").replace("</html>", ""))	
				new_page_html.write(endblock)



	def replace_img_srcs(self):
		images = self.current_img_files
		partials = self.partials
		replaced = []
		for partial in partials:
			soup = BeautifulSoup(open(f"{self.partial_templates}{partial}"), features="html.parser")
			img_sources = [ img for img in soup.find_all("img") ]
			for image_file in images:
				for img in img_sources:
					if image_file in img["src"]:
						img['src'] = get_static_link(image_file, "img")
						replaced.append(img['src'])
						
			with open(f"{self.partial_templates}new_{partial}", "w") as new_partial:
				new_partial.write(str(soup).replace("&quot;", ""))
			os.remove(f"{self.partial_templates}{partial}")
			shutil.move(f"{self.partial_templates}new_{partial}", f"{self.partial_templates}{partial}")
		print(f"\n-----img src replaced...........................\n{replaced}")
			
	
	def move_unclean_to_original(self):
		pages = self.pages
		for page in pages:
			if page.startswith("new_") == False:
				shutil.move(f"{self.main_templates}{page}", f"{self.main}templates/original/{page}")
		for page in pages:
			if page.startswith("new_"):
				os.rename( f"{self.main_templates}{page}", f"{self.main_templates}{page.replace('new_', '')}")

		os.rename(f"{self.main_templates}new_index.html", f"{self.main_templates}index.html" )		



	def add_views(self):
		"""create simple views for all main html pages"""
		files = self.pages
		for file in files:
			with open(f"{self.views}", "a+") as views_py:
				function_text = get_view_text(file)
				views_py.write(function_text)
			
		

	def add_urls(self):
		"""create urls paths for main html pages"""
		files = self.pages
		with open(f"{self.urls}", "a+") as urls_py:
			urls_py.write("from django.urls import path\n")
			urls_py.write("from main import views\n\n\n")
			urls_py.write("#add your url patters here :)\n\n\n")
			urls_py.write(f"app_name = 'main'\n")
			urls_py.write("urlpatterns = [ \n\n")

			urls_text = f"path('', views.index, name='index'),\n"
			urls_py.write(f"\t{urls_text}")
			
			for file in files:
				if file != "index.html":
					urls_text = get_urls_text(file)
					urls_py.write(f"\t{urls_text}")
			
			urls_py.write("\n\n\t\t\t]")

		with open(f"{self.root}/{self.root}/urls.py", "r") as old_url:
			old_url = old_url.read()
			old_url = old_url.replace("from django.urls import path", "from django.urls import path, include")
			old_url = old_url.replace("path('admin/', admin.site.urls),", \
				"path('admin/', admin.site.urls),\npath('', include('main.urls')),")
		
		with open(f"{self.root}/{self.root}/new_urls.py", "w") as new_url:
			new_url.write(old_url)

		os.remove(f"{self.root}/{self.root}/urls.py")
		os.rename(f"{self.root}/{self.root}/new_urls.py", f"{self.root}/{self.root}/urls.py")	
	





	def replace_img_and_page_href(self):
		changed = []
		img_files = self.current_img_files

		for file in self.partials:
			soup = BeautifulSoup(open(f"{self.partial_templates}{file}"), features="html.parser")
			links = [link for link in soup.find_all("a")]
			for link in links:
				
				#change page link "x.html" >>> {% url 'main:x' %}
				try:
					if link['href'] in self.pages:
						link['href'] = get_view_href(file=link['href'])
						change.append(link)
				except:
					pass
				
				#change img link "..assets/x.png" >>> {% static 'img/x.png' %}
				for img in img_files:
					try:
						if img in link['href']:
							link['href'] = get_static_link(file=img, folder="img")
							change.append(link)	

					except:
						pass

			#delete old and write new file			
			soup = str(soup).replace("&quot;", "")
			os.remove(f"{self.partial_templates}{file}")
			with open(f"{self.partial_templates}{file}", "w") as new_file:
				new_file.write(soup)		

		return changed


	def add_static_to_settings(self):
		with open(f"{self.root}/{self.root}/settings.py", "a") as settings_py:
			settings_py.write(get_settings_static_append_text())	

		with open(f"{self.root}/{self.root}/settings.py", "r") as settings_py:	
			old_settings = settings_py.read()
			old_settings = old_settings.replace("'django.contrib.staticfiles',", "'django.contrib.staticfiles',\n'main',\n")
			with open(f"{self.root}/{self.root}/new_settings.py", "w") as new_settings:
				new_settings.write(old_settings)
		os.remove(f"{self.root}/{self.root}/settings.py")		
		os.rename(f"{self.root}/{self.root}/new_settings.py", f"{self.root}/{self.root}/settings.py")	

if __name__ == "__main__":

	# template_name = input(f"{get_folders()}\n\n\n ¿ \
	# Que plantilla quieres usar para el proyecto ?\n")
	
	templates = get_folders()
	for template_name in templates:
		print("--------------------------------", template_name, "--------------------------")
		project = DProject(root=template_name.lower())	
		project.prepare_project()
		btemplate = BTemplate(template=f"{template_name.title()}", project=f"{project.root}")
		project.add_views()
		project.add_urls()
		project.add_static_to_settings()
		project.send_partials()
		project.clean_main_templates()
		btemplate.send_base_html()
		project.replace_img_srcs()
		project.move_unclean_to_original()
		project.replace_img_and_page_href()

	#print("_____________________________________________________________________")
	# for a in dir(project):
	# 	if str(a).startswith("__") == False:
	# 		sleep(3	)
	# 		print(f"---------------------{a}---------------------\n", eval(f"project.{a}"), "\n\n")
	# sleep(50)
	