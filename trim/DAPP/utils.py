import os
from chardet import detect
from time import sleep


load_static = "{% load static %}\n\n"
start_block = "{% block index %}\n\n"
endblock = "\n\n{% endblock %}"
include_start = "{% include"
include_end = "%}"


def extends_base(project):
	extends_base = "{% extends 'base.html' %}\n\n"
	extends_base = extends_base.replace("base.html", f"{project}/base.html")
	return extends_base



def get_include_strin(project_string, partial):
	return f"{include_start} '{project_string}/partials/{partial}.html' {include_end}"


def get_encode_type(file):
	with open(file, 'rb') as f:
		rawdata = f.read()
	return detect(rawdata)['encoding']


def block(html_page):
	"""creates "template block with html string""" 
	start_block = "{% block "
	end_block =  " %}"
	block = f"{start_block}{html_page}{end_block}\n"
	return block






def get_urls_text(file):
	"""get text url path  based on html file"""
	tab = "\t"
	br = "\n"
	url = file[:-5].replace(" ", "-")
	name = file[:-5].replace("-", "_")
	url_text = f"path('{url}/', views.{name}, name='{name}'),\n"
	return url_text


def get_dir_files(root, ending):
	"""get files in one level directory""" 
	files = []
	htmls_list_of_dict = []
	if root == None:
		root = os.getcwd()
	for file in os.listdir(root):
		if file.endswith(ending):
			files.append(file)
	return files


def file_helper(files):
	if type(files) == str:
		files = [str(files)]
	if files[0].endswith("html") == False:
		files = [ file+".html" for file in files ]
	return files


def get_static_link(file, folder):
	start = '"{% '
	end = ' %}"'
	middle = f"static '{folder}/{file}'"
	return start+middle+end


def get_view_href(file, project):
	start = '"{% '
	end = ' %}"'
	unspaced_view = file.replace \
	("-", "_").replace(" ", "_").replace("/", "").replace(".html", "")
	
	middle = f"url '{project}:{unspaced_view}'"
	return start+middle+end




def get_view_text(file, project):
	"""get text of view function base on html file"""
	tab = "\t"
	br = "\n"
	end = "return render(requests, template, context)"
	name = file.replace(".html", "").replace("-", "_")
	context = {'page_title': name.title().replace("-", " ").replace("_", "")}
	template = f"'{project}/main/{file}'"
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




def get_settings_static_append_text():
	append_text = f"\n\nimport os\nBASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
	append_text += "STATIC_URL = '/static/'\n"
	append_text += "#STATIC_ROOT = '/var/www/pytharg.com/static'\n"
	append_text += "STATICFILES_DIRS = [\n"
	append_text += "os.path.join(BASE_DIR, 'static'),\n"
	append_text += "\t]"
	return append_text	

def get_folders(rootdir=None):
	folders = []
	if rootdir == None:
		rootdir = f"{os.getcwd()}/__BOOTSTRAP"
	try:
		for file in os.listdir(rootdir):
			d = os.path.join(rootdir, file)
			if os.path.isdir(d):
				d = d.split("\\")[-1:][0]
				folders.append(d)
	except FileNotFoundError as err:
		print(f"\n<<GOMA no la existe plantilla '{rootdir.split('/')[1]}' !!!!! >>\n")
		print(f"\n<<GOMA no la existe plantilla '{rootdir.split('/')[1]}' !!!!! >>\n")
		print(f"\n<<GOMA no la existe plantilla '{rootdir.split('/')[1]}' !!!!! >>\n")
		print(f"\n<<GOMA no la existe plantilla '{rootdir.split('/')[1]}' !!!!! >>\n")
		raise SystemExit(err)
	#return withdout .git folder		
	return folders[1:]

if __name__ == "__main__":
	 print(get_include_strin(project_string="anyar", partial="services"))