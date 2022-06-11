import os
import shutil
from collections import OrderedDict
from bs4 import BeautifulSoup, Comment
from utils import *
from time import sleep

class BTemplate(object):
	root = None
	project = None
	
	def __init__(self, template, project):
		self.template = f"__BOOTSTRAP/{template}"
		self.project = project
		self.send_main_js()
		self.send_main_css()
		self.send_main_img()
		self.send_main_html()
		self.send_base_html()

	
	@property
	def main_html_files(self):
		html = []
		for root, dirs, files in os.walk(self.template, topdown=False):
			for name in files:
				if name.endswith("html"):
					html.append(name)		
		pages = list(OrderedDict.fromkeys(html))			
		return pages			

	
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
			soup = BeautifulSoup(open(f"{self.project}/main/templates/main/{html}", "rb"), features="html.parser", from_encoding="utf-8")
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
			soup = BeautifulSoup(open(f"{self.project}/main/templates/main/{html}", "rb"), features="html.parser", from_encoding="utf-8")
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
				if (name.endswith("js") and name in required_js) or (name.endswith("js.map")):
					if os.path.exists(f"{self.project}/static/js/{name}") == True:
						if os.path.getsize(f"{self.project}/static/js/{name}") >= \
						os.path.getsize(f"{os.path.join(root, name)}"):
							pass
						else:
							os.remove(f"{self.project}/static/js/{name}")
							shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/js/{name}")
							js.append(name)
					else:
						js.append(name)
						shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/js/{name}")							

		print(f"\n\n-----js sent...........................\n{len(js)}")			

		
		return required_js


	def send_main_css(self):
		css = []
		required_css = self.required_css_files
		for root, dirs, files in os.walk(self.template, topdown=False):
			for name in files:
				if (name.endswith("css") and name in required_css):
					if os.path.exists(f"{self.project}/static/css/{name}") == True:
						if os.path.getsize(f"{self.project}/static/css/{name}") >= \
						os.path.getsize(f"{os.path.join(root, name)}"):
							pass
						else:
							os.remove(f"{self.project}/static/css/{name}")
							shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/css/{name}")
							css.append(name)
					else:
						css.append(name)
						shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/css/{name}")							
	
		print(f"\n-----css sent...........................\n{len(css)}\n")			

		return css
		

	@property
	def required_img_files(self):
		"""returns a list of unduplicated .css files called in main hml pages"""
		required_img_files = []
		for html in self.send_main_html():
			soup = BeautifulSoup(open(f"{self.project}/main/templates/main/{html}", "rb"), features="html.parser", from_encoding="utf-8")
			# print(f"{self.partial_templates}{html}")
			required_img_files += [ a["src"].split("/")[-1:][0] for a in \
			soup.find_all("img") if a['src'].endswith(("jpg", "png", "svg", "gif", "jpeg")) ]
		required_img_files = list(OrderedDict.fromkeys(required_img_files))
		return required_img_files		


	def send_main_img(self):
		img = []
		required_img = self.required_img_files
		print("-----------duplicated images ? ...........\n")
		for root, dirs, files in os.walk(self.template, topdown=False):
			for name in files:
				if name.endswith(("svg", "png", "jpg", "jpeg", "gif")):
					if os.path.exists(f"{self.project}/static/img/{name}") == True:
						if os.path.getsize(f"{self.project}/static/img/{name}") >= \
						os.path.getsize(f"{os.path.join(root, name)}"):
							print(f"duplicated image found: '{name}'")
							pass
						else:
							os.remove(f"{self.project}/static/img/{name}")
							shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/img/{name}")
							img.append(name)
					else:
						img.append(name)
						shutil.copy(f"{os.path.join(root, name)}", f"{self.project}/static/img/{name}")	
	
		print(f"\n-----img files sent...........................\n{len(img)}\n")					

	def send_base_html(self):
		with open("new_base.html", "w", encoding="utf-8") as base:
			soup = BeautifulSoup(open(f"{self.project}/main/templates/main/index.html", "rb"), features="html.parser", from_encoding="utf-8")
			head = soup.find("head")
			links_to_comment = ["remixicon", "boxicons", "bootstrap-icons"]
			
			for link in head.find_all("link"):
				file = link["href"].split("/")[-1:][0]
				
				if file.endswith(".css"):
					link['href'] = f'{get_static_link(file=file, folder="css")}'					
					
					if any(map(file.__contains__, links_to_comment)):
						link = link.replace_with(Comment(str(link)))					
	
				elif file.endswith(("png", "jpg", "jpeg", "svg", "gif")):
					link["href"] = get_static_link(file=file, folder="img")

			boxicons_cdn  = "\n<link href='https://unpkg.com/boxicons@2.1.2/css/boxicons.min.css' rel='stylesheet'>"
			boxicons_link =  BeautifulSoup(boxicons_cdn, features="html.parser")		
			bootstrap_icon_cdn = "\n<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.3/font/bootstrap-icons.css'>"
			bootstrap_icon_link =  BeautifulSoup(bootstrap_icon_cdn, features="html.parser")	
			remixicons_cdn  = "\n<link href='https://cdn.jsdelivr.net/npm/remixicon@2.2.0/fonts/remixicon.css' rel='stylesheet'>"
			remixicons_link =  BeautifulSoup(remixicons_cdn, features="html.parser")		
			
			head.append(Comment("bootstrap icon | remixicon | boxicon CDNs"))
			head.append(boxicons_link)
			head.append(remixicons_link)
			head.append(bootstrap_icon_link)
			
			title = head.find("title")
			title.extract()

			base.write("{% load static %}\n\n")
			base.write(str(head))
			base.write("\n\n<body>\n\n")
			base.write("{% include 'partials/header.html' %}\n\n")

			for page in self.main_html_files:
				base.write(f"{block(page)}")
				base.write("\t{% endblock %}\n\n")

			base.write("{% include 'partials/footer.html' %}\n\n")
			base.write("\n <!-- Javascript Files -->\n")
			for script in soup.find_all("script"):
				if (script["src"].endswith(".js")) and ("https" not in script['src']):
					file = script["src"].split("/")[-1:][0]
					script["src"] = get_static_link(file=file, folder="js")
				base.write(f"\t{str(script)}\n")	
			
			#base.write("\t<script src='https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js' integrity='sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM' crossorigin='anonymous'></script>\n")
			base.write("</body>")	
			
		
		with open(f"{self.project}/main/templates/base.html", "w", encoding="utf-8") as base2:
			with open("new_base.html", "r", encoding="utf-8") as new_base:
				new_base_text = new_base.read()
				new_base_text = new_base_text.replace("&quot;", "")
				base2.write(new_base_text)
		os.remove("new_base.html")		


if __name__ == "__main__":
	print("aca no es!, ABRIR run_single.py o run_all.py")
	sleep(5)