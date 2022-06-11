from DProject import *
from BTemplate import *
from utils import * 


def main():
	templates = get_folders()
	for template_name in templates[48:]:
		print("--------------------------------", template_name, "--------------------------")
		project = DProject(root=template_name.lower())	
		project.prepare_project()
		btemplate = BTemplate(template=f"{template_name.title()}", project=f"{project.root}")
	
		project.add_views()
		project.add_urls()
		project.add_static_to_settings()	
			
		project.replace_img_srcs()	
		project.replace_img_and_page_href()
		project.replace_img_backgrounds()
		project.replace_img_in_css()
	
		btemplate.send_base_html()
		project.send_partials()
		project.clean_main_templates()
		project.move_unclean_to_original()


if __name__ == "__main__":
	main()
	