from DProject import *
from BTemplate import *
from utils import * 
import logging
import traceback

def main():
	templates = get_folders("C:/Users/Abrahan/Desktop/django-trimmer/trim/__BOOTSTRAP")
	print(templates)
	for template_name in templates:
		print("--------------------------------", template_name, "--------------------------")
		try:
			project = DProject(root=template_name.lower())
			project.prepare_app()
			btemplate = BTemplate(template=f"{template_name.title()}", project=f"{project.root}")

			project.add_views()
			project.add_urls()
			project.add_static_to_settings()	
				
			project.replace_img_srcs()	
			project.replace_img_and_page_href()
			project.replace_img_backgrounds()
			project.replace_img_in_css()

			project.send_partials()
			project.clean_main_templates()
			project.move_unclean_to_original()
		
		except Exception as e:
			logging.error(template_name)	
			logging.error(traceback.format_exc())	
							

if __name__ == "__main__":
	main()
	