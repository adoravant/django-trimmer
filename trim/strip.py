from bs4 import BeautifulSoup
from bs4 import Comment
import re
import os
from collections import OrderedDict
import traceback
import logging




# def send_partials(sections):
"""cut sections comment based"""
# 	soup = BeautifulSoup(open("index.html"), features="html.parser")
# 	index_list = []
# 	for section_string in sections:
# 		comments = soup.find_all(string=lambda text: isinstance(text, Comment))
# 		section_range = []
		
# 		for comment in comments:
# 			if re.search(section_string, comment, re.IGNORECASE):
# 				section_range.append(comment)

		
# 		try:
# 			section_start = section_range[0]
# 			section_end = section_range[len(section_range) -1]
# 			index_list.append(section_string)
# 			with open(f"myproject/main/templates/partials/{section_string}.html", "w") as section_html:
# 				with open("index.html" , "r") as html:
# 					lines = html.readlines()
# 					counter = 0
# 					for line in lines:
# 						if section_start in line:
# 							print(f"{section_string}--->>>>>>> tiene section {len(section_range)}")
# 							section_html.write(line)
# 							counter += 1
						
# 						elif (counter >= 1) and (counter <= (len(section_range) -1)):
# 							section_html.write(line)	 
						

# 						if section_end in line:
# 							break

# 						elif (re.search("end", line, re.IGNORECASE)) and (re.search(f"{section_string}", line, re.IGNORECASE)):
# 							break
									
# 			#print(section_string, ": not in file")
# 		except:
# 			print(section_string, ": not in sections")	


# 	return index_list		






# def prepare_index_html(sections=["why-us", "appointment", "services", "doctors", "departments", "gallery", "count", "faq", "testimonial", "about", "contact", "footer", "header"]):
# 	soup = BeautifulSoup(open("myproject/main/templates/main/index.html"), features="html.parser")
# 	with open("myproject/main/templates/main/new_index.html", "w") as new_index:
		
		
		
# 		for section in sections:
# 			try:
# 				div = soup.find(id=re.compile('.*({}).*'.format(section), re.IGNORECASE))
# 				start = "{% includes"
# 				end = " %}"
# 				section_unspaced = section.replace(" ", "-")
# 				include_text = f"\t{start} 'partials/{section_unspaced}.html' {end}\n"
# 				div = div.replace_with(include_text)
# 			except:
# 				print(f"----------------------------{section}------------------------------------------")
# 			# print(div)
# 		new_index.write(str(soup))		

# 	print(soup)		


# def find_sections():
# 	extends_base = "{% extends base.html %}\n\n"
# 	load_static = "{% load static %}\n\n"
# 	start_block = "{% block index %}\n\n"
# 	endblock = "\n\n{% endblock %"
# 	include_start = "{% includes"
# 	include_end = " %}"
	


# 	with open("myproject/main/templates/main/new_index.html", "w") as new_index:
# 		soup = BeautifulSoup(open("myproject/main/templates/main/index.html"), features="html.parser")
# 		head_out = soup.find("head").extract()
# 		scripts_out = [a.extract() for a in soup.find_all("script") ]
		
# 		sections = [ a['id'] for a in soup.find_all("section") ]
# 		sections += ["header", "footer"]

# 		for section in sections:

# 			section_div = soup.find(id=section)
# 			with open(f"myproject/main/templates/partials/{section}.html", "w") as section_html:
# 				section_html.write(load_static)
# 				section_html.write(f"<!-- ======= {section.capitalize()} Section ======= -->\n")
# 				section_html.write(str(section_div.prettify()))
# 				section_html.write(f"\n<!-- ======= End {section.capitalize()} Section ======= -->")
			

# 			section_unspaced = section.replace(" ", "-")
# 			include_text = f"\t{include_start} 'partials/{section_unspaced}.html' {include_end}\n"
# 			if (section == "header") or (section == "footer"):
# 				comment = Comment(f'==== extended from base.html ====-')
# 				section_div = section_div.replace_with(comment)
# 			else:
# 				section_div = section_div.replace_with(include_text)

		
		
# 		new_index.write(extends_base)
# 		new_index.write(load_static)
# 		new_index.write(start_block)
# 		soup = soup.prettify()
# 		new_index.write(str(soup))	
# 		new_index.write(endblock)
	
# 	return sections	


#-------------------------------------------------------------------------------

extends_base = "{% extends 'base.html' %}\n\n"
load_static = "{% load static %}\n\n"
start_block = "{% block index %}\n\n"
endblock = "\n\n{% endblock %"
include_start = "{% includes"
include_end = " %}"




def block(html_page):
	"""creates "template block with html string""" 
	start_block = "{% block "
	end_block =  " %}"
	block = f"{start_block}{html_page}{end_block}\n\n"
	return block



def get_template_sections():
	"""get distinct values_list of sections in all html pages""" 
	files = get_dir_files("myproject/main/templates/main", "html")
	
	sections = []
	for file in files:
		soup = BeautifulSoup(open(f"myproject/main/templates/main/{file}"), features="html.parser")
		page_sections = [ a['id'] for a in soup.find_all("section") ]
		sections += page_sections
	
	sections += ["header", "footer"]	
	html_sections = list(OrderedDict.fromkeys(sections))
	return html_sections	



def get_dir_files(root, ending):
	"""get files in one level directory""" 
	files = []
	htmls_list_of_dict = []
	for file in os.listdir(root):
		if (file.endswith(ending)) and (file not in ["new_index.html"]):
			files.append(file)
	return files		



def send_partials():
	"""send section chunks to indepentant html files"""
	files = get_dir_files("myproject/main/templates/main", "html")
	sections = get_template_sections()

	for section in sections:
		for file in files:
			try:
				soup = BeautifulSoup(open(f"myproject/main/templates/main/{file}"), features="html.parser")
				section_div = soup.find(id=section)
				if section_div != None:
					with open(f"myproject/main/templates/partials/{section}.html", "w") as section_html:
						section_html.write(load_static)
						section_html.write(f"<!-- ======= {section.capitalize()} Section ======= -->\n")
						section_html.write(str(section_div.prettify()))
						section_html.write(f"\n<!-- ======= End {section.capitalize()} Section ======= -->")

			except Exception as e:
				pass
				# logging.error(traceback.format_exc())



def clean_main_templates():
	"""remove reduntant code and add includes to main pages"""
	files = get_dir_files("myproject/main/templates/main", "html")
	sections = get_template_sections()
	
	for file in files:
		soup = BeautifulSoup(open(f"myproject/main/templates/main/{file}"), features="html.parser")
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

		with open(f"myproject/main/templates/main/new_{file}", "w") as new_page_html:
			new_page_html.write(extends_base)
			new_page_html.write(load_static)
			new_page_html.write(block(file))
			soup = soup.prettify()
			new_page_html.write(str(soup))	
			new_page_html.write(endblock)



def add_urls_views(files):
	add_urls(files)
	add_views(files)



def add_views(files):
	"""create simple views for all main html pages"""
	if type(files) == str:
		files = [files]
	for file in files:
		with open("myproject/main/views.py", "a+") as views_py:
			if file.startswith("new") == False:
				function_text = get_function_text(file)
				views_py.write(function_text)
			

def add_urls(files):
	"""create urls paths for main html pages"""
	if type(files) == str:
		files = [files]
	for file in files:
		urls_text = get_urls_text(file)
		if file.startswith("new") == False:
			try:
				with open("myproject/main/urls.py", "r+") as urls_py:
					pass
				with open("myproject/main/urls.py", "a+") as urls_py:
					urls_py.write(f"\t{urls_text}")

			except:
				with open("myproject/main/urls.py", "a+") as urls_py:
					urls_py.write("from django.urls import path\n")
					urls_py.write("import views\n\n\n")
					urls_py.write("#add your url patters here :)\n\n\n")
					urls_py.write("urlpatterns = [ \n\n")
					urls_py.write(f"\t{urls_text}")


				


def get_function_text(file):
	"""get text of view function base on html file"""
	tab = "\t"
	br = "\n"
	end = "return render(requests, template, context)"
	context = {'template':"variable"}
	name = file.replace(".html", "").replace("-", "_")
	template = f"'main/{file}'"
	#define
	func_definition = f"{br}{br}{br}def {name}(requests):{br}"
	func_template = f"{tab}template= {template}{br}"
	func_context = f"{tab}context= {context}{br}"
	funct_end = f"{tab}{end}"

	function_text = func_definition+func_template+func_context+funct_end
	return function_text


def get_urls_text(file):
	"""get text url path  based on html file"""
	tab = "\t"
	br = "\n"
	url = file[:-5].replace(" ", "-")
	name = file[:-5].replace("-", "_")
	url_text = f"path('{url}/', views.{name}, name='{name}'),\n"
	return url_text



def remove_views_py(files):
	"""removes unmodified view based on html files"""
	files = file_helper(files)
	with open("myproject/main/views.py", "r+") as views_py:
		read_text = views_py.read()
		with open("myproject/main/new_views.py", "w") as new_views_py:
			for file in files:
				function_text = get_function_text(file)
				while function_text in read_text:
					read_text = read_text.replace(function_text, "")
					print(read_text, "_________________________________________")
			new_views_py.write(read_text)
	try:
		os.remove("myproject/main/old_views.py")
	except:
		pass #amigo
	os.rename("myproject/main/views.py", "myproject/main/old_views.py")
	os.rename("myproject/main/new_views.py", "myproject/main/views.py")




def find_links(files):
	"""return "hrefs" takes sections or html partial"""
	"""returns img, page, inpage links"""
	files = file_helper(files)
	links, img_links, page_links, inpage_links = [], [], [], []
	for file in files:
		soup = BeautifulSoup(open(f"myproject/main/templates/partials/{file}"), features="html.parser")
		links += [link for link in soup.find_all("a")]
		
		for a in links:
			try:
				if a["href"].endswith(".html"):
					page_links.append(a['href'])
				if  a["href"].endswith((".jpg", ".png", ".jpeg", "svg", "gif")):
					img_links.append(a['href'])	
				if ( a['href'].startswith("#")) and ( len(a['href']) >= 2 ):	
					inpage_links.append(a['href'])

			except:
				#logging.error(traceback.format_exc())
				pass		
		
		#delete duplicates
	img_links = list(OrderedDict.fromkeys(img_links))
	page_links = list(OrderedDict.fromkeys(page_links))
	inpage_links = list(OrderedDict.fromkeys(inpage_links))
	return img_links, page_links, inpage_links



def find_images(files):
	"""returns images "srcs" in images"""
	files = file_helper(files)
	all_images = []
	for file in files:
		soup = BeautifulSoup(open(f"myproject/main/templates/partials/{file}"), features="html.parser")
		images = soup.find_all("img")
		all_images += images

	image_srcs = list(OrderedDict.fromkeys([a["src"] for a in all_images]))
	return image_srcs
	


def file_helper(files):
	if type(files) == str:
		files = [str(files)]
	if files[0].endswith("html") == False:
		files = [ file+".html" for file in files ]
	return files		




def setup():
	print(sections)
	send_partials()
	clean_main_templates()
	files = get_dir_files("myproject/main/templates/main", "html")
	print(files)
	for file in files:
		add_views(file)
		add_urls(file)
	remove_views_py(["testimonials.html", "blog-single.html"])



if __name__ == "__main__":
	sections = get_template_sections()
	setup()
	# print(sections)
	# send_partials()
	# clean_main_templates()
	# files = get_dir_files("myproject/main/templates/main", "html")
	# print(files)
	# for file in files:
	# 	add_views(file)
	# 	add_urls(file)
	# remove_views_py(["testimonials.html", "blog-single.html"])
	images = find_images(sections)
	for image in images:
		print(image)
	links = find_links(sections)
	for link in links:
		print(link)