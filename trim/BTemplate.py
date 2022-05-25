
import os
import shutil
from collections import OrderedDict
from bs4 import BeautifulSoup
from utils import *

class BTemplate(object):
	root = None
	project = None
	
	def __init__(self, template, project):
		self.template = template
		self.project = project
		self.send_main_js()
		self.send_main_css()
		self.send_main_img()
		self.send_main_html()

	def send_main_html(self):
		html = []
		for root, dirs, files in os.walk(self.template, topdown=False):
			for name in files:
				if name.endswith("html"):
					html.append(name)	
					if os.path.exists(f"{self.project}/main/templates/main/{name}") == True:
						if os.path.getsize(f"{self.project}/main/templates/main/{name}") >= \
						os.path.getsize(f"{os.path.join(root, name)}"):
							pass
						else:
							os.remove(f"{self.project}/main/templates/main/{name}")
							shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/main/templates/main/{name}")
			
					else:
						shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/main/templates/main/{name}")		
					
		pages = list(OrderedDict.fromkeys(html))			
		return pages

	@property
	def required_css_files(self):
		"""returns a list of unduplicated .css files called in main hml pages"""
		required_css_files = []
		for html in self.send_main_html():
			soup = BeautifulSoup(open(f"{self.project}/main/templates/main/{html}"), features="html.parser")
			# print(f"{self.partial_templates}{html}")
			required_css_files += [ a["href"].split("/")[-1:][0] for a in \
			soup.find_all("link") if a['href'].endswith("css") ]
		required_css_files = list(OrderedDict.fromkeys(required_css_files))
		return required_css_files




	@property
	def required_js_files(self):
		"""returns a list of unduplicated .css files called in main hml pages"""
		required_js_files = []
		for html in self.send_main_html():
			soup = BeautifulSoup(open(f"{self.project}/main/templates/main/{html}"), features="html.parser")
			# print(f"{self.partial_templates}{html}")
			required_js_files += [ a["src"].split("/")[-1:][0] for a in \
			soup.find_all("script") if a['src'].endswith(".js") ]
		scripts = list(OrderedDict.fromkeys(required_js_files))
		return scripts					

	

	def send_main_js(self):
		js = []
		required_js = self.required_js_files
		for root, dirs, files in os.walk(self.template, topdown=False):
			for name in files:
				pass
				if name.endswith("js") and name in required_js:
					if os.path.exists(f"{self.project}/static/js/{name}") == True:
						if os.path.getsize(f"{self.project}/static/js/{name}") >= \
						os.path.getsize(f"{os.path.join(root, name)}"):
							print("pass", name)
							pass
						else:
							os.remove(f"{self.project}/static/js/{name}")
							shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/js/{name}")
			
					else:
						shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/js/{name}")							
		print(required_js)			



	def send_main_css(self):
		css = []
		required_css = self.required_css_files
		for root, dirs, files in os.walk(self.template, topdown=False):
			for name in files:
				pass
				if name.endswith("css") and name in required_css:
					if os.path.exists(f"{self.project}/static/css/{name}") == True:
						if os.path.getsize(f"{self.project}/static/css/{name}") >= \
						os.path.getsize(f"{os.path.join(root, name)}"):
							print("pass", name)
							pass
						else:
							os.remove(f"{self.project}/static/css/{name}")
							shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/css/{name}")
			
					else:
						shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/css/{name}")							
		print(required_css)		



	@property
	def required_img_files(self):
		"""returns a list of unduplicated .css files called in main hml pages"""
		required_img_files = []
		for html in self.send_main_html():
			soup = BeautifulSoup(open(f"{self.project}/main/templates/main/{html}"), features="html.parser")
			# print(f"{self.partial_templates}{html}")
			required_img_files += [ a["src"].split("/")[-1:][0] for a in \
			soup.find_all("img") if a['src'].endswith(("jpg", "png", "svg", "gif", "jpeg")) ]
		required_img_files = list(OrderedDict.fromkeys(required_img_files))
		return required_img_files		




	def send_main_img(self):
		img = []
		required_img = self.required_img_files
		for root, dirs, files in os.walk(self.template, topdown=False):
			for name in files:
				pass
				if name.endswith(("svg", "png", "jpg", "jpeg", "gif")) and name in required_img:
					if os.path.exists(f"{self.project}/static/img/{name}") == True:
						if os.path.getsize(f"{self.project}/static/img/{name}") >= \
						os.path.getsize(f"{os.path.join(root, name)}"):
							print("pass", name)
							pass
						else:
							os.remove(f"{self.project}/static/img/{name}")
							shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/img/{name}")
			
					else:
						shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/img/{name}")	



	def send_base_html(self):
		with open("new_base.html", 'w') as base:
			soup = BeautifulSoup(open(f"{self.project}/main/templates/main/index.html"), features="html.parser")
			head = soup.find("head")
			for link in head.find_all("link"):
				if link["href"].endswith(("css", "png", "jpg", "gif", "svg", "jpeg")):
					file = link["href"].split("/")[-1:][0]
					link["href"] = get_static_link(file=file, folder="css")

			base.write(str(head))
			base.write("\n\n<body>\n\n")
			base.write("{% include 'partials/header.html' %}\n\n")

			for page in self.send_main_html():
				base.write(f"{block(page)}")
				base.write("\t{% endblock %}\n\n")

			base.write("\n{% include 'partials/footer.html' %}\n")
			base.write("\n <!-- Javascript Files -->\n")
			for script in soup.find_all("script"):
				if (script["src"].endswith(".js")) and ("https" not in script['src']):
					file = script["src"].split("/")[-1:][0]
					script["src"] = get_static_link(file=file, folder="js")
				base.write(f"{str(script)}\n")	
			base.write("</body>")	
		
		with open(f"{self.project}/main/templates/base.html", 'w') as base2:
			with open("new_base.html", 'r') as new_base:
				new_base_text = new_base.read()
				new_base_text = new_base_text.replace("&quot;", "")
				base2.write(new_base_text)


