from DProject import DProject
import os
import shutil
from collections import OrderedDict
from bs4 import BeautifulSoup

class BTemplate(object):
	root = None
	project = None
	
	def __init__(self, template, project):
		self.template = template
		self.project = project

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
							os.remove(f"{project}/main/templates/main/{name}")
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



if __name__ == "__main__":
	btemplate = BTemplate(template="Company", project="myproject")
	print(btemplate.send_main_js())
	print(btemplate.send_main_img())
	print(btemplate.send_main_html())
	print(btemplate.send_main_css())

