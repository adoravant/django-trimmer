import os
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

	
	
	def get_dir_files(dir, ending):
		"""get files in one level directory""" 
		files = []
		for file in os.listdir(f"{dir}"):
			if (file.endswith(ending)):
				files.append(file)
		return files	

	
	@property
	def css_files(self):
		css_files = self.get_dir_files(dir=f"{self.static}css", ending="css")
		return css_files

	@property	
	def js_files(self):
		js_files = self.get_dir_files(dir=f"{self.static}js", ending="js")
		return js_files

	@property	
	def img_files(self):
		css_files = self.get_dir_files(dir=f"{self.static}img", ending=("jpg", ".jpeg", ".png", ".gif", ".svg"))
		return img_files	
	
	@property		
	def partials(self):
		partial_templates = self.get_dir_files(dir=f"{self.partial_templates}", ending=(".html"))
		return partial_templates
	
	@property		
	def pages(self):
		pages = self.get_dir_files(dir=f"{self.main_templates}", ending=(".html"))
		return pages

