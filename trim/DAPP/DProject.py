import os, shutil
import re
from bs4 import BeautifulSoup, Comment
from collections import OrderedDict
from utils import *
import logging
from BTemplate import BTemplate
import traceback
from time import sleep

class DProject(object):
	root = None
	project = None
	instances = []
	

	def __init__(self, root, project="pytharg"):
		self.project = project
		self.root = root
		self.static = f"{self.project}/static/{self.root}/"
		self.main_templates = f"{self.project}/templates/{self.root}/main/"
		self.partial_templates = f"{self.project}/templates/{self.root}/partials/"
		self.original = f"{self.project}/templates/{self.root}/original/"
		self.urls = f"{self.project}/{self.root}/urls.py"
		self.views = f"{self.project}/{self.root}/views.py"
		self.__class__.instances.append(self)

		

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
	def pages(self):
		"""returns list of htmls in /main"""
		pages = get_dir_files(root=f"{self.main_templates}", ending=(".html"))
		return pages


	@property	
	def sections(self):
		"""returns list of unduplicaded section ids in main pages"""
		sections = []
		for page in self.pages:
			page_sections = []
			soup = BeautifulSoup(open(f"{self.main_templates}{page}"), features="html.parser")
			for section_div in soup.find_all("section"):
				try:
					page_sections.append(section_div['id'])
				except:
					#CHEQUEAR POR QUE NO ESTA TRAYENDO UNA SOLA CLASE
					section_div['id'] = section_div['class'][0]	
					page_sections.append(section_div['id'])
			sections += page_sections
		sections += ["header", "footer"]	
		sections = list(OrderedDict.fromkeys(sections))
		return sections			


	@property		
	def partials(self):
		"""returns list of htmls in  /partials"""
		partial_templates = get_dir_files(root=f"{self.partial_templates}", ending=(".html"))
		return partial_templates



	def send_partials(self):
		"""send section chunks to indepentant html files"""
		sections = self.sections
		files = self.pages
		for section in sections:
			for file in files:
				try:
					soup = BeautifulSoup(open(f"{self.main_templates}{file}", "rb"), from_encoding="utf-8", features="html.parser")
					section_div = soup.find(id=section)
					if section_div != None:
						with open(f"{self.partial_templates}{section}.html", "w", encoding="utf-8") as section_html:
							section_html.write(load_static)
							section_html.write(f"<!-- ======= {section.capitalize()} Section ======= -->\n")
							section_html.write(str(section_div.prettify()))
							section_html.write(f"\n<!-- ======= End {section.capitalize()} Section ======= -->")
				except Exception as e:
					pass
					logging.error(traceback.format_exc())

		print(f"\n-------partials sent.............................\n{self.partials}\n")
		return self.partials			


	def clean_main_templates(self):
		sections = self.sections
		files = self.pages	
		for file in files:
			soup = BeautifulSoup(open(f"{self.main_templates}{file}", "rb"), from_encoding="utf-8", features="html.parser")
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
						include_text = get_include_strin(project_string=self.root, partial=f"{section_unspaced}")

						if (section == "header") or (section == "footer"):
							comment = Comment(f'==== extended from base.html ====-')
							section_div = section_div.replace_with(comment)
						else:
							section_div = section_div.replace_with(include_text)
						
				
				except Exception as e:
					logging.error(traceback.format_exc())
					pass


			with open(f"{self.main_templates}new_{file}", "w", encoding="utf-8") as new_page_html:
				new_page_html.write(extends_base(self.root))
				new_page_html.write(load_static)
				new_page_html.write(block(file))
				new_page_html.write("\n<head>\n\t<title>{{ page_title }}</title>\n</head>")
				soup = soup.prettify()
				new_page_html.write(str(soup).replace('<html lang="en">', '').replace("<!DOCTYPE html>", "").replace("</html>", ""))	
				new_page_html.write(endblock)



	def replace_img_srcs(self):
		images = self.current_img_files
		pages = self.pages
		replaced = []
		for page in pages:
			soup = BeautifulSoup(open(f"{self.main_templates}{page}", "rb"), from_encoding="utf-8", features="html.parser")
			img_sources = [ img for img in soup.find_all("img") ]
			for image_file in images:
				for img in img_sources:
					if image_file in img["src"]:
						img['src'] = get_static_link(image_file, f"{self.root}/img")
						replaced.append(img['src'])
						
			with open(f"{self.main_templates}new_{page}", "w", encoding="utf-8") as new_page:
				new_page.write(str(soup).replace("&quot;", ""))
			os.remove(f"{self.main_templates}{page}")
			shutil.move(f"{self.main_templates}new_{page}", f"{self.main_templates}{page}")
		try:
			print(f"\n-----img src replaced...........................\n{len(replaced)}")
		except:
			print(f"\n-----img src replacedxxxxxxxxxxxxxxxxxxxxxxxxxxx\n[]")	
			
	
	def move_unclean_to_original(self):
		pages = self.pages
		for page in pages:
			if page.startswith("new_") == False:
				shutil.move(f"{self.main_templates}{page}", f"{self.original}{page}")
		for page in pages:
			if page.startswith("new_"):
				os.rename( f"{self.main_templates}{page}", f"{self.main_templates}{page.replace('new_', '')}")
		try:		
			os.rename(f"{self.main_templates}new_index.html", f"{self.main_templates}index.html" )		
		except:
			pass


	def add_views(self):
		"""create simple views for all main html pages"""
		files = self.pages
		for file in files:
			with open(f"{self.views}", "a+") as views_py:
				function_text = get_view_text(file, self.root)
				views_py.write(function_text)
			
		

	def add_urls(self):
		"""create urls paths for main html pages"""
		files = self.pages
		with open(f"{self.urls}", "a+") as urls_py:
			urls_py.write("from django.urls import path\n")
			urls_py.write(f"from {self.root} import views\n\n\n")
			urls_py.write("#add your url patters here :)\n\n\n")
			urls_py.write(f"app_name = '{self.root}'\n")
			urls_py.write("urlpatterns = [ \n\n")

			urls_text = f"path('', views.index, name='index'),\n"
			urls_py.write(f"\t{urls_text}")
			
			for file in files:
				if file != "index.html":
					urls_text = get_urls_text(file)
					urls_py.write(f"\t{urls_text}")
			
			urls_py.write("\n\n\t\t\t]")

		with open(f"{self.project}/{self.project}/urls.py", "r", encoding="utf-8") as old_url:
			old_url = old_url.read()
			old_url = old_url.replace("from django.urls import path", "from django.urls import path, include")
			
			old_url = old_url.replace("path('admin/', admin.site.urls),", \
				f"path('admin/', admin.site.urls),\n\tpath('{self.root}/', include('{self.root}.urls')),")
		
		with open(f"{self.project}/{self.project}/new_urls.py", "a", encoding="utf-8") as new_url:
			new_url.write(old_url)

		os.remove(f"{self.project}/{self.project}/urls.py")
		os.rename(f"{self.project}/{self.project}/new_urls.py", f"{self.project}/{self.project}/urls.py")	
	





	def replace_img_and_page_href(self):
		changed = []
		img_files = self.current_img_files

		for page in self.pages:
			soup = BeautifulSoup(open(f"{self.main_templates}{page}", "rb"), from_encoding='utf-8', features="html.parser")
			links = [link for link in soup.find_all("a")]
			for link in links:
				
				#change page link "x.html" >>> {% url 'main:x' %}
				try:
					if link['href'] in self.pages:
						link['href'] = get_view_href(file=link['href'], project=self.root)
						change.append(link)
				except:
					pass
				
				#change img link "..assets/x.png" >>> {% static 'img/x.png' %}
				for img in img_files:
					try:
						if img in link['href']:
							link['href'] = get_static_link(file=img, folder=f"{self.root}/img")
							change.append(link)	

					except:
						pass

			#delete old and write new file			
			soup = str(soup).replace("&quot;", "")
			os.remove(f"{self.main_templates}{page}")
			with open(f"{self.main_templates}{page}", "w", encoding="utf-8") as new_file:
				new_file.write(soup)		

		return changed


	def add_static_to_settings(self):
		with open(f"{self.project}/{self.project}/settings.py", "a", encoding="utf-8") as settings_py:
			settings_py.write(get_settings_static_append_text())	

		with open(f"{self.project}/{self.project}/settings.py", "r", encoding="utf-8") as settings_py:	
			old_settings = settings_py.read()
			old_settings = old_settings.replace("'django.contrib.staticfiles',", f"'django.contrib.staticfiles',\n\t'{self.root}',")
			with open(f"{self.project}/{self.project}/new_settings.py", "w", encoding="utf-8") as new_settings:
				new_settings.write(old_settings)
		os.remove(f"{self.project}/{self.project}/settings.py")		
		os.rename(f"{self.project}/{self.project}/new_settings.py", f"{self.project}/{self.project}/settings.py")	
		
		#solo para ayuda en consola en ejecucion __main__:
		

	
	def replace_img_backgrounds(self):
		for page in self.pages:
			soup = BeautifulSoup(open(f"{self.main_templates}{page}", "rb"), from_encoding="utf-8", features="html.parser")
			divs = soup.find_all("div")
			for div in divs:
				try:
					#if more than on style
					if ";" in div['style']:
						style_list =  div['style'].split(";")
						for style_item in style_list:
							if "background-image:" in style_item:
								old_folder = style_item.split("(")[1][:-1]
								file_name = old_folder.split("/")[-1:][0]
								new_folder = f"'/static/{self.root}/img/{file_name}'"
								div['style'] = div['style'].replace(old_folder, new_folder)
				
					else:
						old_folder = div['style'].split("(")[1][:-1]
						file_name = old_folder.split("/")[-1:][0]
						new_folder = f"static/{self.root}/img/{file_name}"
					div['style'] = div['style'].replace(old_folder, new_folder)
						
				except:
					pass
				with open(f"{self.main_templates}new_{page}", "w", encoding="utf-8") as new_page:
					new_page.write(str(soup))
				os.remove(f"{self.main_templates}{page}")
				os.rename(f"{self.main_templates}new_{page}", f"{self.main_templates}{page}")



	def replace_img_in_css(self):
		pattern = r"\(.*(?i:jpg.|gif.|png.|bmp.|svg.|jpeg.);?"
		css_list = get_dir_files(f"{self.static}css", ".css")
		css_list = [item for item in css_list if item != "aos.css"]
		css_file = min(css_list, key=len)
		with open(f"{self.static}css/{css_file}", "r", encoding="utf-8") as old:
			old_styles = old.read()
			old_paths = [ x.replace("(", "").replace('"', "") for x in re.findall(pattern, old_styles) ]
			for old_path in old_paths:
				new_path = f"/static/{self.root}/img/{ old_path.split('/')[-1:][0] }"
				old_styles = old_styles.replace(old_path, new_path)

		os.remove(f"{self.static}css/{css_file}")
		with open(f"{self.static}css/{css_file}", "w", encoding="utf-8") as new_style:
			new_style.write(old_styles)		

	def prepare_app(self):
		start_dir = os.getcwd()
		os.chdir(self.project)
		try:
			shutil.rmtree(self.root)
			os.system(f"manage.py startapp {self.root}")
		except:
			os.system(f"manage.py startapp {self.root}")
		
		try:
			os.mkdir(f"templates/{self.root}/")
		except:
			shutil.rmtree(f"templates/{self.root}")
			os.mkdir(f"templates/{self.root}/")
		
		try:
			os.mkdir(f"static/{self.root}")
		except:
			shutil.rmtree(f"static/{self.root}")
			os.mkdir(f"static/{self.root}")	

		os.mkdir(f"templates/{self.root}/main")
		os.mkdir(f"templates/{self.root}/partials")
		os.mkdir(f"templates/{self.root}/original")
		os.mkdir(f"static/{self.root}/css")
		os.mkdir(f"static/{self.root}/img")
		os.mkdir(f"static/{self.root}/js")
		os.chdir(start_dir)

if __name__ == "__main__":
	p = DProject(project="pytharg", root="anyar")
	p.prepare_app()